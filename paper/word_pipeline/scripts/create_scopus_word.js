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

const INPUT = "paper/paper_full.md";
const OUTPUT = "paper/word_pipeline/docx/paper_scopus.docx";

function splitTableLine(line) {
  return line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((c) => c.trim());
}

function isSeparatorLine(line) {
  const cells = splitTableLine(line);
  return cells.length > 0 && cells.every((c) => /^:?-{3,}:?$/.test(c));
}

function stripMd(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "$1")
    .replace(/\*(.*?)\*/g, "$1")
    .replace(/`([^`]+)`/g, "$1");
}

function parseInlineRuns(text) {
  const runs = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  let idx = 0;
  let m = re.exec(text);
  while (m) {
    if (m.index > idx) {
      runs.push(new TextRun({ text: text.slice(idx, m.index) }));
    }
    const token = m[0];
    if (token.startsWith("**") && token.endsWith("**")) {
      runs.push(new TextRun({ text: token.slice(2, -2), bold: true }));
    } else if (token.startsWith("*") && token.endsWith("*")) {
      runs.push(new TextRun({ text: token.slice(1, -1), italics: true }));
    } else if (token.startsWith("`") && token.endsWith("`")) {
      runs.push(new TextRun({ text: token.slice(1, -1), font: "Courier New" }));
    }
    idx = m.index + token.length;
    m = re.exec(text);
  }
  if (idx < text.length) runs.push(new TextRun({ text: text.slice(idx) }));
  return runs.length ? runs : [new TextRun("")];
}

function tableFromRows(rows) {
  const cols = rows[0].length;
  const width = Math.floor(9360 / cols);
  const border = { style: BorderStyle.SINGLE, size: 1, color: "D0D0D0" };

  return new Table({
    columnWidths: Array(cols).fill(width),
    rows: rows.map((r, i) =>
      new TableRow({
        tableHeader: i === 0,
        children: r.map((c) =>
          new TableCell({
            width: { size: width, type: WidthType.DXA },
            borders: { top: border, bottom: border, left: border, right: border },
            shading: i === 0 ? { fill: "EFEFEF", type: ShadingType.CLEAR } : undefined,
            children: [
              new Paragraph({
                alignment: i === 0 ? AlignmentType.CENTER : AlignmentType.LEFT,
                children: [new TextRun({ text: stripMd(c), bold: i === 0 })],
              }),
            ],
          })
        ),
      })
    ),
  });
}

function parseMarkdown(md) {
  const lines = md.replace(/\r\n/g, "\n").split("\n");
  const children = [];
  let i = 0;
  let inCode = false;
  let inReferences = false;

  while (i < lines.length) {
    const raw = lines[i];
    const line = raw.trim();

    if (line.startsWith("<!--") && line.endsWith("-->")) {
      i += 1;
      continue;
    }

    if (/^```/.test(line)) {
      inCode = !inCode;
      i += 1;
      continue;
    }

    if (inCode) {
      children.push(
        new Paragraph({
          style: "BodyText",
          children: [new TextRun({ text: raw, font: "Courier New", size: 20 })],
        })
      );
      i += 1;
      continue;
    }

    if (!line) {
      children.push(new Paragraph({ style: "BodyText", children: [new TextRun("")] }));
      i += 1;
      continue;
    }

    if (/^---+$/.test(line)) {
      i += 1;
      continue;
    }

    const h = line.match(/^(#{1,6})\s+(.*)$/);
    if (h) {
      const level = h[1].length;
      const text = stripMd(h[2]);
      if (/references/i.test(text)) inReferences = true;
      const heading =
        level === 1
          ? HeadingLevel.TITLE
          : level === 2
            ? HeadingLevel.HEADING_1
            : level === 3
              ? HeadingLevel.HEADING_2
              : HeadingLevel.HEADING_3;
      children.push(
        new Paragraph({
          heading,
          children: [new TextRun(text)],
          alignment: level === 1 ? AlignmentType.CENTER : AlignmentType.LEFT,
        })
      );
      i += 1;
      continue;
    }

    if (raw.includes("|") && i + 1 < lines.length && isSeparatorLine(lines[i + 1])) {
      const rows = [splitTableLine(raw)];
      i += 2;
      while (i < lines.length && lines[i].includes("|")) {
        const row = splitTableLine(lines[i]);
        if (row.length !== rows[0].length) break;
        rows.push(row);
        i += 1;
      }
      children.push(tableFromRows(rows));
      continue;
    }

    if (/^-\s+/.test(line)) {
      children.push(
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          style: "BodyText",
          children: parseInlineRuns(line.replace(/^-\s+/, "")),
        })
      );
      i += 1;
      continue;
    }

    if (/^>\s+/.test(line)) {
      children.push(
        new Paragraph({
          style: "QuoteText",
          children: parseInlineRuns(line.replace(/^>\s+/, "")),
        })
      );
      i += 1;
      continue;
    }

    if (/^\*\*Authors:\*\*/.test(line) || /^\*\*Affiliations:\*\*/.test(line) || /^\*\*\*Corresponding author:\*\*/.test(line) || /^\*\*Keywords:\*\*/.test(line)) {
      children.push(
        new Paragraph({
          style: "MetaText",
          children: parseInlineRuns(line),
          alignment: /^\*\*Keywords:\*\*/.test(line) ? AlignmentType.JUSTIFIED : AlignmentType.CENTER,
        })
      );
      i += 1;
      continue;
    }

    if (inReferences) {
      children.push(
        new Paragraph({
          style: "ReferenceText",
          children: parseInlineRuns(line),
        })
      );
      i += 1;
      continue;
    }

    children.push(
      new Paragraph({
        style: "BodyText",
        children: parseInlineRuns(line),
      })
    );
    i += 1;
  }
  return children;
}

const content = fs.readFileSync(INPUT, "utf8");
const children = parseMarkdown(content);

const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Times New Roman", size: 24 } },
      paragraph: { spacing: { line: 276, after: 120 } },
    },
    paragraphStyles: [
      {
        id: "Title",
        name: "Title",
        basedOn: "Normal",
        run: { font: "Times New Roman", size: 32, bold: true },
        paragraph: { alignment: AlignmentType.CENTER, spacing: { after: 180, line: 276 } },
      },
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "BodyText",
        quickFormat: true,
        run: { font: "Times New Roman", size: 28, bold: true },
        paragraph: { spacing: { before: 180, after: 120, line: 276 }, outlineLevel: 0 },
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "BodyText",
        quickFormat: true,
        run: { font: "Times New Roman", size: 26, bold: true },
        paragraph: { spacing: { before: 120, after: 80, line: 276 }, outlineLevel: 1 },
      },
      {
        id: "Heading3",
        name: "Heading 3",
        basedOn: "Normal",
        next: "BodyText",
        quickFormat: true,
        run: { font: "Times New Roman", size: 24, bold: true },
        paragraph: { spacing: { before: 100, after: 60, line: 276 }, outlineLevel: 2 },
      },
      {
        id: "BodyText",
        name: "Body Text",
        basedOn: "Normal",
        run: { font: "Times New Roman", size: 24 },
        paragraph: {
          alignment: AlignmentType.JUSTIFIED,
          spacing: { line: 276, after: 120 },
          indent: { firstLine: 720 },
        },
      },
      {
        id: "MetaText",
        name: "Meta Text",
        basedOn: "Normal",
        run: { font: "Times New Roman", size: 22 },
        paragraph: { alignment: AlignmentType.CENTER, spacing: { after: 80, line: 240 } },
      },
      {
        id: "QuoteText",
        name: "Quote Text",
        basedOn: "Normal",
        run: { font: "Times New Roman", size: 24, italics: true },
        paragraph: {
          alignment: AlignmentType.LEFT,
          indent: { left: 720 },
          spacing: { line: 276, after: 100 },
        },
      },
      {
        id: "ReferenceText",
        name: "Reference Text",
        basedOn: "Normal",
        run: { font: "Times New Roman", size: 22 },
        paragraph: {
          alignment: AlignmentType.LEFT,
          spacing: { line: 240, after: 60 },
          indent: { left: 540, hanging: 540 },
        },
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
        page: {
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
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
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });
