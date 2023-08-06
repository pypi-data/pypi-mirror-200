# Copyright (C) 2021,2022,2023 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Convert and back source text file into text as well."""

import argparse
import gettext
import logging
from datetime import datetime as dt
from pathlib import Path

from txt2ebook.helpers import lower_underscore
from txt2ebook.models import Book, Chapter, Volume

logger = logging.getLogger(__name__)


class TxtWriter:
    """Module for writing ebook in txt format."""

    def __init__(self, book: Book, opts: argparse.Namespace) -> None:
        """Create a TxtWriter module.

        Args:
            book(Book): The book model which contains metadata and table of
            contents of volumes and chapters.
            opts(argparse.Namespace): The configs from the command-line.

        Returns:
            None
        """
        self.book = book
        self.config = opts

        self.filename = opts.input_file.name
        self.overwrite = opts.overwrite
        self.split_volume_and_chapter = opts.split_volume_and_chapter
        self.paragraph_separator = opts.paragraph_separator
        self.with_toc = opts.with_toc

        self._load_translation()

    def _load_translation(self):
        localedir = Path(Path(__file__).parent.parent, "locales")
        translation = gettext.translation(
            "txt2ebook", localedir=localedir, languages=[self.config.language]
        )
        self._ = translation.gettext

    def write(self) -> None:
        """Optionally backup and overwrite the txt file.

        If the input content came from stdin, we'll skip backup and overwrite
        source text file.
        """
        if self.filename == "<stdin>":
            logger.info("Skip backup source text file as content from stdin")
        elif self.split_volume_and_chapter:
            self._export_multiple_files()
        else:
            if self.overwrite:
                self._overwrite_file()
            else:
                self._new_file()

    def _export_multiple_files(self) -> None:
        logger.info("Split multiple files")

        txt_filename = Path(self.filename)
        export_filename = Path(
            txt_filename.resolve().parent.joinpath(
                lower_underscore(
                    f"00_{txt_filename.stem}_" + self._("metadata") + ".txt"
                )
            )
        )
        logger.info("Creating %s", export_filename)
        with open(export_filename, "w", encoding="utf8") as file:
            file.write(self._to_metadata_txt())

        sc_seq = 1
        if self.with_toc:
            export_filename = Path(
                txt_filename.resolve().parent.joinpath(
                    lower_underscore(
                        f"01_{txt_filename.stem}_" + self._("toc") + ".txt"
                    )
                )
            )
            logger.info("Creating %s", export_filename)
            with open(export_filename, "w", encoding="utf8") as file:
                file.write(self._to_toc())

            sc_seq = 2

        for section in self.book.toc:
            section_seq = str(sc_seq).rjust(2, "0")

            ct_seq = 0
            if isinstance(section, Volume):
                for chapter in section.chapters:
                    chapter_seq = str(ct_seq).rjust(2, "0")
                    filename = lower_underscore(
                        (
                            f"{section_seq}"
                            f"_{chapter_seq}"
                            f"_{txt_filename.stem}"
                            f"_{section.title}"
                            f"_{chapter.title}"
                            ".txt"
                        )
                    )

                    export_filename = Path(
                        txt_filename.resolve().parent.joinpath(filename)
                    )
                    logger.info("Creating %s", export_filename)
                    with open(export_filename, "w", encoding="utf8") as file:
                        file.write(
                            self._to_volume_chapter_txt(section, chapter)
                        )
                    ct_seq = ct_seq + 1
            if isinstance(section, Chapter):
                filename = lower_underscore(
                    (
                        f"{section_seq}"
                        f"_{txt_filename.stem}"
                        f"_{section.title}"
                        ".txt"
                    )
                )

                export_filename = Path(
                    txt_filename.resolve().parent.joinpath(filename)
                )
                logger.info("Creating %s", export_filename)
                with open(export_filename, "w", encoding="utf8") as file:
                    file.write(self._to_chapter_txt(section))

            sc_seq = sc_seq + 1

    def _new_file(self) -> None:
        txt_filename = Path(self.filename)

        ymd_hms = dt.now().strftime("%Y%m%d_%H%M%S")
        new_filename = Path(
            txt_filename.resolve().parent.joinpath(
                lower_underscore(txt_filename.stem + "_" + ymd_hms + ".txt")
            )
        )

        with open(new_filename, "w", encoding="utf8") as file:
            file.write(self._to_txt())
            logger.info("Create txt file: %s", new_filename.resolve())

    def _overwrite_file(self) -> None:
        txt_filename = Path(self.filename)

        with open(txt_filename, "w", encoding="utf8") as file:
            file.write(self._to_txt())
            logger.info("Overwrite txt file: %s", txt_filename.resolve())

    def _to_txt(self) -> str:
        toc = self._to_toc() if self.with_toc else ""
        return self._to_metadata_txt() + toc + self._to_body_txt()

    def _to_toc(self) -> str:
        toc = []
        toc.append(self._("toc") + "\n")

        for section in self.book.toc:
            if isinstance(section, Volume):
                toc.append(section.title)
                for chapter in section.chapters:
                    toc.append(chapter.title)
            if isinstance(section, Chapter):
                toc.append(section.title)

        return "\n- ".join(toc) + self.paragraph_separator

    def _to_metadata_txt(self) -> str:
        metadata = [
            self._("title:") + self.book.title,
            self._("author:") + "，".join(self.book.authors),
            self._("tag:") + "，".join(self.book.tags),
        ]
        return "\n".join(metadata) + self.paragraph_separator

    def _to_body_txt(self) -> str:
        content = []
        for section in self.book.toc:
            if isinstance(section, Volume):
                content.append(self._to_volume_txt(section))
            if isinstance(section, Chapter):
                content.append(self._to_chapter_txt(section))

        return f"{self.paragraph_separator}".join(content)

    def _to_volume_txt(self, volume) -> str:
        return (
            volume.title
            + self.paragraph_separator
            + self.paragraph_separator.join(
                [self._to_chapter_txt(chapter) for chapter in volume.chapters]
            )
        )

    def _to_chapter_txt(self, chapter) -> str:
        return (
            chapter.title
            + self.paragraph_separator
            + self.paragraph_separator.join(chapter.paragraphs)
        )

    def _to_volume_chapter_txt(self, volume, chapter) -> str:
        return (
            volume.title
            + " "
            + chapter.title
            + self.paragraph_separator
            + self.paragraph_separator.join(chapter.paragraphs)
        )
