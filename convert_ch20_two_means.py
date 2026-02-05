#!/usr/bin/env python3
"""
Convert inference-two-means.qmd to PreTeXt format
"""

import re
import sys

def escape_xml(text):
    """Escape special XML characters"""
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def process_math(text):
    """Convert inline and display math to PreTeXt format"""
    # Display math $$...$$ to <me>...</me>
    text = re.sub(r'\$\$([^\$]+)\$\$', r'<me>\1</me>', text)
    # Inline math $...$ to <m>...</m>
    text = re.sub(r'\$([^\$]+)\$', r'<m>\1</m>', text)
    return text

def convert_cross_refs(text):
    """Convert @fig-, @tbl-, @sec- references to xref"""
    patterns = [
        (r'@fig-([a-zA-Z0-9\-]+)', r'<xref ref="fig-\1"/>'),
        (r'@tbl-([a-zA-Z0-9\-]+)', r'<xref ref="tbl-\1"/>'),
        (r'@sec-([a-zA-Z0-9\-]+)', r'<xref ref="sec-\1"/>'),
    ]
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    return text

def convert_index(text):
    """Convert \index{} to <idx> tags"""
    # Handle nested index entries like \index{point estimate!difference in means}
    def idx_replace(match):
        content = match.group(1)
        parts = content.split('!')
        if len(parts) == 1:
            return f'<idx>{parts[0]}</idx>'
        else:
            result = '<idx>'
            for i, part in enumerate(parts):
                result += f'<h>{part}</h>'
            result += '</idx>'
            return result
    
    text = re.sub(r'\\index\{([^}]+)\}', idx_replace, text)
    return text

def process_header_line(line):
    """Convert markdown headers to PreTeXt section tags"""
    if line.startswith('# '):
        title = line[2:].strip()
        # Extract id if present
        id_match = re.search(r'\{#([^}]+)\}', title)
        if id_match:
            section_id = id_match.group(1)
            title = re.sub(r'\s*\{#[^}]+\}', '', title)
            return f'<chapter xml:id="{section_id}">\n<title>{title}</title>\n\n<introduction>'
        return f'<chapter>\n<title>{title}</title>\n\n<introduction>'
    elif line.startswith('## '):
        title = line[3:].strip()
        id_match = re.search(r'\{#([^}]+)\}', title)
        if id_match:
            section_id = id_match.group(1)
            title = re.sub(r'\s*\{#[^}]+\}', '', title)
            return f'</section>\n\n<section xml:id="{section_id}">\n<title>{title}</title>'
        return f'</section>\n\n<section>\n<title>{title}</title>'
    elif line.startswith('### '):
        title = line[4:].strip()
        id_match = re.search(r'\{#([^}]+)\}', title)
        if id_match:
            section_id = id_match.group(1)
            title = re.sub(r'\s*\{#[^}]+\}', '', title)
            return f'</subsection>\n\n<subsection xml:id="{section_id}">\n<title>{title}</title>'
        return f'</subsection>\n\n<subsection>\n<title>{title}</title>'
    return line

def main():
    input_file = '/home/runner/work/ims/ims/inference-two-means.qmd'
    output_file = '/home/runner/work/ims/ims/source/chapters/ch20-inference-two-independent-means.ptx'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Start building output
    output_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    output_lines.append('<chapter xml:id="sec-inference-two-means" xmlns:xi="http://www.w3.org/2001/XInclude">')
    output_lines.append('')
    output_lines.append('<title>Inference for comparing two independent means</title>')
    output_lines.append('')
    
    # Process the file line by line
    lines = content.split('\n')
    
    in_code_block = False
    in_chapterintro = False
    in_guidedpractice = False
    in_workedexample = False
    in_data_note = False
    in_important = False
    in_solution = False
    code_buffer = []
    para_buffer = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip initial setup code blocks
        if i < 20 and line.startswith('```{r}'):
            while i < len(lines) and not lines[i].startswith('```'):
                i += 1
            i += 1
            continue
        
        # Handle chapter intro
        if '::: {.chapterintro' in line:
            output_lines.append('<introduction>')
            in_chapterintro = True
            i += 1
            continue
        
        if in_chapterintro and line.strip() == ':::':
            output_lines.append('</introduction>')
            in_chapterintro = False
            i += 1
            continue
        
        # Handle R code blocks
        if line.startswith('```{r}'):
            in_code_block = True
            code_buffer = []
            label = ''
            caption = ''
            # Look for label and caption
            j = i + 1
            while j < len(lines) and lines[j].startswith('#|'):
                if 'label:' in lines[j]:
                    label = lines[j].split('label:')[1].strip()
                elif 'fig-cap:' in lines[j] or 'tbl-cap:' in lines[j]:
                    caption = lines[j].split('cap:')[1].strip()
                j += 1
            i = j
            continue
        
        if in_code_block:
            if line.startswith('```'):
                in_code_block = False
                # Output as listing
                if code_buffer:
                    if label:
                        output_lines.append(f'<listing xml:id="{label}">')
                    else:
                        output_lines.append('<listing>')
                    if caption:
                        clean_cap = caption.strip('`"\'')
                        output_lines.append(f'  <caption>{clean_cap}</caption>')
                    output_lines.append('  <program language="r">')
                    output_lines.append('    <code>')
                    for code_line in code_buffer:
                        # Escape XML in code
                        escaped = code_line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        output_lines.append(escaped)
                    output_lines.append('    </code>')
                    output_lines.append('  </program>')
                    output_lines.append('</listing>')
                    output_lines.append('')
                code_buffer = []
                i += 1
                continue
            else:
                code_buffer.append(line)
                i += 1
                continue
        
        # Handle guided practice
        if '::: {.guidedpractice' in line:
            output_lines.append('<exercise>')
            output_lines.append('  <statement>')
            in_guidedpractice = True
            i += 1
            continue
        
        # Handle worked example
        if '::: {.workedexample' in line:
            output_lines.append('<example>')
            output_lines.append('  <statement>')
            in_workedexample = True
            i += 1
            continue
        
        # Handle data notes
        if '::: {.data' in line:
            output_lines.append('<note>')
            output_lines.append('  <title>Data</title>')
            in_data_note = True
            i += 1
            continue
        
        # Handle important boxes
        if '::: {.important' in line:
            output_lines.append('<assemblage>')
            in_important = True
            i += 1
            continue
        
        # Handle solutions within exercises
        if in_guidedpractice or in_workedexample:
            if '::: {.callout-note collapse="true"}' in line:
                i += 1
                if i < len(lines) and '## Solution' in lines[i]:
                    output_lines.append('  </statement>')
                    output_lines.append('  <solution>')
                    in_solution = True
                    i += 1
                    continue
        
        # Handle closing of sections
        if line.strip() == ':::':
            if in_solution:
                output_lines.append('  </solution>')
                in_solution = False
            if in_guidedpractice:
                output_lines.append('</exercise>')
                output_lines.append('')
                in_guidedpractice = False
            elif in_workedexample:
                output_lines.append('</example>')
                output_lines.append('')
                in_workedexample = False
            elif in_data_note:
                output_lines.append('</note>')
                output_lines.append('')
                in_data_note = False
            elif in_important:
                output_lines.append('</assemblage>')
                output_lines.append('')
                in_important = False
            i += 1
            continue
        
        # Process regular content lines
        if line.strip():
            # Convert markdown formatting
            processed = convert_cross_refs(line)
            processed = convert_index(processed)
            processed = process_math(processed)
            
            # Wrap in paragraph if needed
            if not processed.startswith('<') and not in_code_block:
                if in_guidedpractice or in_workedexample or in_solution:
                    output_lines.append(f'    <p>{processed}</p>')
                else:
                    output_lines.append(f'  <p>{processed}</p>')
            else:
                output_lines.append(processed)
        
        i += 1
    
    # Close any open tags
    output_lines.append('')
    output_lines.append('</chapter>')
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"Conversion complete: {output_file}")

if __name__ == '__main__':
    main()
