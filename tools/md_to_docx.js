#!/usr/bin/env node
// Convert the exam review markdown to a .docx. Usage: node md_to_docx.js in.md out.docx
const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType,
        AlignmentType, BorderStyle, LevelFormat, Footer, PageNumber } = require('docx');

const [,, inPath, outPath] = process.argv;
const md = fs.readFileSync(inPath, 'utf8').split('\n');
const PAGE_W = 11906, PAGE_H = 16838, MARGIN = 1134;        // A4, 2 cm margins
const CONTENT_W = PAGE_W - 2 * MARGIN;                       // 9638 DXA

function inline(text, base = {}) {
  const runs = [], re = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) runs.push(new TextRun({ ...base, text: text.slice(last, m.index) }));
    const tok = m[0];
    if (tok.startsWith('**')) runs.push(new TextRun({ ...base, text: tok.slice(2, -2), bold: true }));
    else runs.push(new TextRun({ ...base, text: tok.slice(1, -1), font: 'Consolas', size: (base.size || 22) - 2 }));
    last = m.index + tok.length;
  }
  if (last < text.length) runs.push(new TextRun({ ...base, text: text.slice(last) }));
  return runs;
}

function table(rows) {
  const parse = r => r.replace(/^\|/, '').replace(/\|\s*$/, '').split('|').map(c => c.trim());
  const header = parse(rows[0]), body = rows.slice(2).map(parse), ncol = header.length;
  let widths;
  if (ncol === 8) widths = [650, 2650, 1250, 1050, 1000, 900, 1100, 1038];
  else if (ncol === 3) widths = [4238, 2200, 3200];
  else { const w = Math.floor(CONTENT_W / ncol); widths = Array(ncol).fill(w); widths[ncol - 1] += CONTENT_W - w * ncol; }
  const size = ncol >= 6 ? 17 : 20;
  const mk = (cells, isHeader) => new TableRow({ tableHeader: isHeader, children: cells.map((c, idx) => new TableCell({
    width: { size: widths[idx], type: WidthType.DXA },
    shading: isHeader ? { type: ShadingType.CLEAR, fill: 'D9E2F3', color: 'auto' } : undefined,
    margins: { top: 40, bottom: 40, left: 70, right: 70 },
    children: [new Paragraph({ spacing: { after: 0 }, children: inline(c, isHeader ? { bold: true, size } : { size }) })],
  })) });
  return new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: widths,
    rows: [mk(header, true), ...body.map(r => mk(r, false))] });
}

const hr = () => new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '999999', space: 1 } }, spacing: { before: 120, after: 240 } });
const isBlock = l => !l.trim() || l.startsWith('|') || /^#/.test(l) || /^- /.test(l) || /^\d+\.\s/.test(l) || /^---+$/.test(l.trim());

const children = [];
let i = 0;
while (i < md.length) {
  const line = md[i];
  if (!line.trim()) { i++; continue; }
  if (line.startsWith('|')) { const rows = []; while (i < md.length && md[i].startsWith('|')) rows.push(md[i++]); children.push(table(rows), new Paragraph({ spacing: { after: 120 } })); continue; }
  if (/^---+$/.test(line.trim())) { children.push(hr()); i++; continue; }
  const h = line.match(/^(#{1,3})\s+(.*)$/);
  if (h) {
    let text = h[2]; if (text === 'Files') text = 'Files in the repository';
    const lvl = [HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3][h[1].length - 1];
    children.push(new Paragraph({ heading: lvl, children: inline(text), keepNext: true })); i++; continue;
  }
  if (/^- /.test(line)) {
    let text = line.slice(2); i++;
    while (i < md.length && !isBlock(md[i])) text += ' ' + md[i++].trim();
    children.push(new Paragraph({ numbering: { reference: 'bullets', level: 0 }, children: inline(text), spacing: { after: 80 } })); continue;
  }
  const n = line.match(/^(\d+)\.\s+(.*)$/);
  if (n) {
    let text = n[2]; i++;
    while (i < md.length && !isBlock(md[i])) text += ' ' + md[i++].trim();
    children.push(new Paragraph({ indent: { left: 567, hanging: 360 }, spacing: { after: 100 }, children: [new TextRun({ text: n[1] + '.\t', bold: true }), ...inline(text)] })); continue;
  }
  const buf = [line]; i++;
  while (i < md.length && !isBlock(md[i])) buf.push(md[i++]);
  children.push(new Paragraph({ children: inline(buf.join(' ')), spacing: { after: 140 } }));
}

const doc = new Document({
  title: 'PRINCE2 7 Practitioner Mock Exam (Version A): full review',
  styles: {
    default: { document: { run: { font: 'Calibri', size: 22 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: 'Calibri', size: 36, bold: true, color: '1F3864' }, paragraph: { spacing: { before: 240, after: 200 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: 'Calibri', size: 28, bold: true, color: '2F5496' }, paragraph: { spacing: { before: 360, after: 140 }, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: 'Calibri', size: 24, bold: true, color: '1F3864' }, paragraph: { spacing: { before: 280, after: 100 }, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 567, hanging: 283 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ size: 18, color: '666666', children: ['PRINCE2 7 Practitioner mock exam review    |    Page ', PageNumber.CURRENT, ' of ', PageNumber.TOTAL_PAGES] })] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(outPath, buf); console.log('wrote', outPath, buf.length, 'bytes,', children.length, 'blocks'); });
