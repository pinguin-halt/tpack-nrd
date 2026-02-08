const fs = require("fs");
const {
  AlignmentType,
  BorderStyle,
  Document,
  HeadingLevel,
  LevelFormat,
  Packer,
  Paragraph,
  ShadingType,
  Table,
  TableCell,
  TableRow,
  TextRun,
  WidthType,
} = require("docx");

const INPUT = "drafts/paper_outline.md";
const OUTPUT = "drafts/paper_outline.docx";

function splitTableLine(line) {
  const raw = line.trim().replace(/^\|/, "").replace(/\|$/, "");
  return raw.split("|").map((c) => c.trim());
}

function isSeparatorLine(line) {
  const cells = splitTableLine(line);
  if (cells.length === 0) return false;
  return cells.every((c) => /^:?-{3,}:?$/.test(c));
}

function cleanInline(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "$1")
    .replace(/\*(.*?)\*/g, "$1")
    .replace(/`([^`]+)`/g, "$1");
}

function toHeadingLevel(n) {
  if (n === 1) return HeadingLevel.HEADING_1;
  if (n === 2) return HeadingLevel.HEADING_2;
  if (n === 3) return HeadingLevel.HEADING_3;
  return HeadingLevel.HEADING_4;
}

function makeTable(rows) {
  const colCount = rows[0].length;
  const colWidth = Math.floor(9360 / colCount);
  const border = { style: BorderStyle.SINGLE, size: 1, color: "D9D9D9" };

  return new Table({
    columnWidths: Array(colCount).fill(colWidth),
    rows: rows.map((row, ri) =>
      new TableRow({
        tableHeader: ri === 0,
        children: row.map((cell) =>
          new TableCell({
            width: { size: colWidth, type: WidthType.DXA },
            borders: { top: border, bottom: border, left: border, right: border },
            shading:
              ri === 0
                ? { fill: "EAF2F8", type: ShadingType.CLEAR }
                : undefined,
            children: [
              new Paragraph({
                alignment: ri === 0 ? AlignmentType.CENTER : AlignmentType.LEFT,
                children: [
                  new TextRun({ text: cleanInline(cell), bold: ri === 0 }),
                ],
              }),
            ],
          })
        ),
      })
    ),
  });
}

function parseMarkdownToDocChildren(md) {
  const lines = md.replace(/\r\n/g, "\n").split("\n");
  const children = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    if (!trimmed) {
      children.push(new Paragraph({ children: [new TextRun("")] }));
      i += 1;
      continue;
    }

    if (/^#{1,6}\s+/.test(trimmed)) {
      const m = trimmed.match(/^(#{1,6})\s+(.*)$/);
      const level = m[1].length;
      const text = cleanInline(m[2]);
      children.push(
        new Paragraph({
          heading: toHeadingLevel(level),
          children: [new TextRun(text)],
        })
      );
      i += 1;
      continue;
    }

    if (
      line.includes("|") &&
      i + 1 < lines.length &&
      isSeparatorLine(lines[i + 1])
    ) {
      const tableRows = [];
      tableRows.push(splitTableLine(lines[i]));
      i += 2;
      while (i < lines.length && lines[i].includes("|")) {
        const row = splitTableLine(lines[i]);
        if (row.length === tableRows[0].length) tableRows.push(row);
        else break;
        i += 1;
      }
      children.push(makeTable(tableRows));
      continue;
    }

    if (/^-\s+/.test(trimmed)) {
      children.push(
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun(cleanInline(trimmed.replace(/^-\s+/, "")))],
        })
      );
      i += 1;
      continue;
    }

    if (/^>\s+/.test(trimmed)) {
      children.push(
        new Paragraph({
          children: [
            new TextRun({ text: cleanInline(trimmed.replace(/^>\s+/, "")), italics: true }),
          ],
        })
      );
      i += 1;
      continue;
    }

    if (/^```/.test(trimmed)) {
      i += 1;
      while (i < lines.length && !/^```/.test(lines[i].trim())) {
        children.push(
          new Paragraph({
            children: [
              new TextRun({ text: lines[i], font: "Courier New", size: 20 }),
            ],
          })
        );
        i += 1;
      }
      i += 1;
      continue;
    }

    if (/^---+$/.test(trimmed)) {
      children.push(new Paragraph({ children: [new TextRun("")] }));
      i += 1;
      continue;
    }

    children.push(
      new Paragraph({ children: [new TextRun(cleanInline(trimmed))] })
    );
    i += 1;
  }

  return children;
}

const markdown = fs.readFileSync(INPUT, "utf8");
const children = parseMarkdownToDocChildren(markdown);

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } },
    paragraphStyles: [
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 34, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 },
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 30, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 180, after: 120 }, outlineLevel: 1 },
      },
      {
        id: "Heading3",
        name: "Heading 3",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 28, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 120, after: 80 }, outlineLevel: 2 },
      },
    ],
  },
  numbering: {
    config: [
      {
        reference: "bullet-list",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "•",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } },
          },
        ],
      },
    ],
  },
  sections: [
    {
      properties: {
        page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } },
      },
      children,
    },
  ],
});

Packer.toBuffer(doc)
  .then((buffer) => {
    fs.writeFileSync(OUTPUT, buffer);
    console.log(`Sukses: ${OUTPUT}`);
  })
  .catch((err) => {
    console.error(err);
    process.exit(1);
  });
