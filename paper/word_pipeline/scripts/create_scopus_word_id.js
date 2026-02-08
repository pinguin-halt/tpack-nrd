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

const SOURCES = [
  "drafts/paper_outline.md",
  "drafts/results_rm1_id.md",
  "drafts/results_rm2_rm5_id.md",
];
const OUTPUT = "paper/word_pipeline/docx/paper_scopus_id.docx";

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

function inlineRuns(text) {
  const runs = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  let idx = 0;
  let m = re.exec(text);
  while (m) {
    if (m.index > idx) runs.push(new TextRun({ text: text.slice(idx, m.index) }));
    const t = m[0];
    if (t.startsWith("**")) runs.push(new TextRun({ text: t.slice(2, -2), bold: true }));
    else if (t.startsWith("*")) runs.push(new TextRun({ text: t.slice(1, -1), italics: true }));
    else runs.push(new TextRun({ text: t.slice(1, -1), font: "Courier New" }));
    idx = m.index + t.length;
    m = re.exec(text);
  }
  if (idx < text.length) runs.push(new TextRun({ text: text.slice(idx) }));
  return runs.length ? runs : [new TextRun("")];
}

function imageType(file) {
  const ext = path.extname(file).toLowerCase();
  if (ext === ".jpg") return "jpeg";
  if (ext === ".jpeg") return "jpeg";
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

function parseOneMarkdown(filePath) {
  const md = fs.readFileSync(filePath, "utf8").replace(/\r\n/g, "\n");
  const base = path.dirname(filePath);
  const lines = md.split("\n");
  const children = [];
  let i = 0;
  let inCode = false;

  while (i < lines.length) {
    const raw = lines[i];
    const line = raw.trim();

    if (/^```/.test(line)) {
      inCode = !inCode;
      i += 1;
      continue;
    }
    if (inCode) {
      children.push(
        new Paragraph({ style: "BodyText", children: [new TextRun({ text: raw, font: "Courier New", size: 20 })] })
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
      const heading =
        level === 1
          ? HeadingLevel.HEADING_1
          : level === 2
            ? HeadingLevel.HEADING_2
            : HeadingLevel.HEADING_3;
      children.push(new Paragraph({ heading, children: [new TextRun(text)] }));
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

    const img = line.match(/^!\[(.*?)\]\((.*?)\)$/);
    if (img) {
      const caption = img[1] || "Gambar";
      const rel = img[2];
      const full = path.resolve(base, rel);
      if (fs.existsSync(full)) {
        const data = fs.readFileSync(full);
        children.push(
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new ImageRun({
                type: imageType(full),
                data,
                transformation: { width: 520, height: 330 },
                altText: { title: caption, description: caption, name: caption },
              }),
            ],
          })
        );
        children.push(
          new Paragraph({
            style: "FigureCaption",
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: caption, italics: true })],
          })
        );
      } else {
        children.push(
          new Paragraph({
            style: "BodyText",
            children: [new TextRun(`[Gambar tidak ditemukan: ${rel}]`)],
          })
        );
      }
      i += 1;
      continue;
    }

    if (/^-\s+/.test(line)) {
      children.push(
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          style: "BodyText",
          children: inlineRuns(line.replace(/^-\s+/, "")),
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
          children: inlineRuns(line.replace(/^\d+\.\s+/, "")),
        })
      );
      i += 1;
      continue;
    }

    children.push(new Paragraph({ style: "BodyText", children: inlineRuns(line) }));
    i += 1;
  }

  return children;
}

const allChildren = [];
allChildren.push(
  new Paragraph({
    heading: HeadingLevel.TITLE,
    alignment: AlignmentType.CENTER,
    children: [
      new TextRun({
        text: "Naskah Indonesia (Draf): PjBL, TPACK, STEM, ESD, dan RPP Integratif",
        bold: true,
      }),
    ],
  })
);
allChildren.push(
  new Paragraph({
    style: "MetaText",
    alignment: AlignmentType.CENTER,
    children: [
      new TextRun({
        text: "Dokumen ini disusun otomatis dari outline dan draf hasil analisis Indonesia.",
      }),
    ],
  })
);

for (const src of SOURCES) {
  allChildren.push(
    new Paragraph({
      style: "MetaText",
      children: [new TextRun({ text: `Sumber: ${src}`, italics: true })],
    })
  );
  allChildren.push(...parseOneMarkdown(src));
}

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
        id: "MetaText",
        name: "Meta Text",
        basedOn: "Normal",
        run: { font: "Times New Roman", size: 22 },
        paragraph: { alignment: AlignmentType.LEFT, spacing: { line: 240, after: 80 } },
      },
      {
        id: "FigureCaption",
        name: "Figure Caption",
        basedOn: "Normal",
        run: { font: "Times New Roman", size: 20, italics: true },
        paragraph: { alignment: AlignmentType.CENTER, spacing: { line: 240, after: 120 } },
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
      properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
      children: allChildren,
    },
  ],
});

Packer.toBuffer(doc)
  .then((buf) => {
    fs.writeFileSync(OUTPUT, buf);
    console.log(`Sukses: ${OUTPUT}`);
  })
  .catch((err) => {
    console.error(err);
    process.exit(1);
  });
