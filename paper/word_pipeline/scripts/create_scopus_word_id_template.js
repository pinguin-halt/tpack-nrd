const fs = require("fs");
const path = require("path");
const {
  AlignmentType,
  BorderStyle,
  Document,
  HeadingLevel,
  ImageRun,
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

const INPUT = "paper/paper_full_id.md";
const OUTPUT = "paper/word_pipeline/docx/paper_full_id_scopus_template.docx";

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
    if (m.index > idx) runs.push(new TextRun({ text: text.slice(idx, m.index) }));
    const token = m[0];
    if (token.startsWith("**")) {
      runs.push(new TextRun({ text: token.slice(2, -2), bold: true }));
    } else if (token.startsWith("*")) {
      runs.push(new TextRun({ text: token.slice(1, -1), italics: true }));
    } else {
      runs.push(new TextRun({ text: token.slice(1, -1), font: "Courier New" }));
    }
    idx = m.index + token.length;
    m = re.exec(text);
  }
  if (idx < text.length) runs.push(new TextRun({ text: text.slice(idx) }));
  return runs.length ? runs : [new TextRun("")];
}

function imageType(file) {
  const ext = path.extname(file).toLowerCase();
  if (ext === ".jpg" || ext === ".jpeg") return "jpeg";
  if (ext === ".gif") return "gif";
  if (ext === ".bmp") return "bmp";
  if (ext === ".svg") return "svg";
  return "png";
}

function makeTable(rows) {
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

function parseMarkdown(filePath) {
  const md = fs.readFileSync(filePath, "utf8").replace(/\r\n/g, "\n");
  const baseDir = path.dirname(filePath);
  const lines = md.split("\n");
  const children = [];
  let i = 0;
  let inCode = false;
  let inReferences = false;

  while (i < lines.length) {
    const raw = lines[i];
    const line = raw.trim();

    if (!line) {
      children.push(new Paragraph({ style: "BodyText", children: [new TextRun("")] }));
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

    if (/^---+$/.test(line)) {
      i += 1;
      continue;
    }

    const img = line.match(/^!\[(.*?)\]\((.*?)\)$/);
    if (img) {
      const caption = img[1] || "Gambar";
      const target = path.resolve(baseDir, img[2]);
      if (fs.existsSync(target)) {
        const data = fs.readFileSync(target);
        children.push(
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new ImageRun({
                type: imageType(target),
                data,
                transformation: { width: 520, height: 320 },
                altText: { title: caption, description: caption, name: caption },
              }),
            ],
          })
        );
        children.push(
          new Paragraph({
            style: "CaptionText",
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: caption, italics: true })],
          })
        );
      }
      i += 1;
      continue;
    }

    const h = line.match(/^(#{1,6})\s+(.*)$/);
    if (h) {
      const lvl = h[1].length;
      const text = stripMd(h[2]);
      if (text.toLowerCase().includes("daftar pustaka")) inReferences = true;
      const heading =
        lvl === 1
          ? HeadingLevel.TITLE
          : lvl === 2
            ? HeadingLevel.HEADING_1
            : lvl === 3
              ? HeadingLevel.HEADING_2
              : HeadingLevel.HEADING_3;
      children.push(
        new Paragraph({
          heading,
          alignment: lvl === 1 ? AlignmentType.CENTER : AlignmentType.LEFT,
          children: [new TextRun(text)],
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
      children.push(makeTable(rows));
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

    if (/^\d+\.\s+/.test(line)) {
      children.push(
        new Paragraph({
          numbering: { reference: "number-list", level: 0 },
          style: "BodyText",
          children: parseInlineRuns(line.replace(/^\d+\.\s+/, "")),
        })
      );
      i += 1;
      continue;
    }

    if (inReferences && /^[A-Z].*\(\d{4}\)\./.test(line)) {
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

const children = parseMarkdown(INPUT);

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
        paragraph: { alignment: AlignmentType.CENTER, spacing: { line: 276, after: 180 } },
      },
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "BodyText",
        quickFormat: true,
        run: { font: "Times New Roman", size: 28, bold: true },
        paragraph: { spacing: { before: 180, after: 100, line: 276 }, outlineLevel: 0 },
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
        paragraph: { spacing: { before: 80, after: 60, line: 276 }, outlineLevel: 2 },
      },
      {
        id: "BodyText",
        name: "Body Text",
        basedOn: "Normal",
        run: { font: "Times New Roman", size: 24 },
        paragraph: { alignment: AlignmentType.JUSTIFIED, spacing: { line: 276, after: 120 } },
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
      {
        id: "CaptionText",
        name: "Caption Text",
        basedOn: "Normal",
        run: { font: "Times New Roman", size: 20, italics: true },
        paragraph: { alignment: AlignmentType.CENTER, spacing: { line: 240, after: 100 } },
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
      {
        reference: "number-list",
        levels: [
          {
            level: 0,
            format: LevelFormat.DECIMAL,
            text: "%1.",
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
