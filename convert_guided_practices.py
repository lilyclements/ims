#!/usr/bin/env python3
"""
Convert guided practice blocks from foundations-mathematical.qmd to PreTeXt format
and insert them into ch13-inference-mathematical-models.ptx
"""

import re

# Line numbers for each guided practice block in the qmd file
GP_LINES = [139, 348, 457, 479, 493, 579, 677, 752, 869, 884, 959, 971, 1035, 1054, 1318, 1452]

def read_file(filename):
    """Read file and return lines"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.readlines()

def extract_gp_block(lines, start_line):
    """Extract guided practice block starting at given line (1-indexed)"""
    idx = start_line - 1  # Convert to 0-indexed
    
    # Verify we're at the start of a GP block
    if not lines[idx].strip().startswith('::: {.guidedpractice'):
        raise ValueError(f"Line {start_line} is not a guided practice block start")
    
    # Extract the question (lines between opening ::: and the callout-note)
    question_lines = []
    idx += 1
    while idx < len(lines):
        line = lines[idx].strip()
        if line.startswith('::: {.callout-note'):
            break
        if line and line != ':::':
            question_lines.append(lines[idx].rstrip())
        idx += 1
    
    # Extract the solution (inside callout-note, after ## Solution)
    solution_lines = []
    in_solution = False
    while idx < len(lines):
        line = lines[idx].strip()
        if line == ':::' and in_solution:
            # End of callout-note
            idx += 1
            if idx < len(lines) and lines[idx].strip() == ':::':
                # End of guidedpractice block
                break
        elif line.startswith('## Solution'):
            in_solution = True
            idx += 1
            # Skip blank line after ## Solution
            if idx < len(lines) and not lines[idx].strip():
                idx += 1
            continue
        elif in_solution and line:
            solution_lines.append(lines[idx].rstrip())
        idx += 1
    
    return {
        'question': '\n'.join(question_lines),
        'solution': '\n'.join(solution_lines)
    }

def convert_to_ptx(text):
    """Convert markdown text to PreTeXt format"""
    # Handle inline math $x$ -> <m>x</m>
    text = re.sub(r'\$([^\$]+)\$', r'<m>\1</m>', text)
    
    # Handle bold **text** -> <alert>text</alert>
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<alert>\1</alert>', text)
    
    # Handle italic *text* -> <em>text</em> (but not already in tags)
    text = re.sub(r'(?<![<\w])\*([^\*]+)\*(?![>\w])', r'<em>\1</em>', text)
    
    # Handle code `text` -> <c>text</c>
    text = re.sub(r'`([^`]+)`', r'<c>\1</c>', text)
    
    # Handle cross-refs @fig-xxx -> <xref ref="fig-xxx" />
    text = re.sub(r'@fig-([a-zA-Z0-9_-]+)', r'<xref ref="fig-\1" />', text)
    text = re.sub(r'@tbl-([a-zA-Z0-9_-]+)', r'<xref ref="tbl-\1" />', text)
    
    # Handle section refs [Chapter -@sec-xxx] -> <xref ref="sec-xxx" text="title" />
    text = re.sub(r'\[Chapter -@sec-([a-zA-Z0-9_-]+)\]', r'<xref ref="sec-\1" text="title" />', text)
    
    # Escape XML entities
    text = text.replace('&', '&amp;')
    # But fix double-escaping
    text = text.replace('&amp;amp;', '&amp;')
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    # But restore our XML tags
    text = text.replace('&lt;m&gt;', '<m>').replace('&lt;/m&gt;', '</m>')
    text = text.replace('&lt;alert&gt;', '<alert>').replace('&lt;/alert&gt;', '</alert>')
    text = text.replace('&lt;em&gt;', '<em>').replace('&lt;/em&gt;', '</em>')
    text = text.replace('&lt;c&gt;', '<c>').replace('&lt;/c&gt;', '</c>')
    text = text.replace('&lt;xref ', '<xref ').replace(' /&gt;', ' />')
    
    return text

def create_exercise_xml(gp_data):
    """Create PreTeXt exercise element from guided practice data"""
    question = convert_to_ptx(gp_data['question'].strip())
    solution = convert_to_ptx(gp_data['solution'].strip())
    
    # Split into paragraphs if there are blank lines
    question_paras = [p.strip() for p in question.split('\n\n') if p.strip()]
    solution_paras = [p.strip() for p in solution.split('\n\n') if p.strip()]
    
    # If single line items like (a), (b), create a list
    def format_content(paras):
        result = []
        for para in paras:
            # Check if this is a list item
            lines = para.split('\n')
            if len(lines) > 1 and all(re.match(r'^\([a-z]\)', l.strip()) for l in lines if l.strip()):
                # It's a list
                result.append('      <ol>')
                for line in lines:
                    if line.strip():
                        content = re.sub(r'^\([a-z]\)\s*', '', line.strip())
                        result.append(f'        <li><p>{content}</p></li>')
                result.append('      </ol>')
            else:
                # Regular paragraph(s)
                for line in lines:
                    if line.strip():
                        result.append(f'      <p>{line.strip()}</p>')
        return '\n'.join(result)
    
    question_xml = format_content(question_paras)
    solution_xml = format_content(solution_paras)
    
    xml = f"""    <exercise>
      <title>Guided Practice</title>
      <statement>
{question_xml}
      </statement>
      <solution>
{solution_xml}
      </solution>
    </exercise>"""
    
    return xml

def main():
    # Read the qmd file
    qmd_lines = read_file('/home/runner/work/ims/ims/foundations-mathematical.qmd')
    
    # Extract all guided practice blocks
    print("Extracting guided practice blocks...")
    gp_blocks = []
    for line_num in GP_LINES:
        print(f"  Line {line_num}...")
        gp_data = extract_gp_block(qmd_lines, line_num)
        gp_blocks.append({
            'line': line_num,
            'data': gp_data,
            'xml': create_exercise_xml(gp_data)
        })
    
    # Print the extracted blocks for verification
    for i, block in enumerate(gp_blocks, 1):
        print(f"\n{'='*60}")
        print(f"GP {i} (line {block['line']}):")
        print(f"Question: {block['data']['question'][:100]}...")
        print(f"Solution: {block['data']['solution'][:100]}...")
        print(f"\nXML:\n{block['xml']}")
    
    print(f"\n{'='*60}")
    print(f"\nTotal: {len(gp_blocks)} guided practice blocks extracted")

if __name__ == '__main__':
    main()
