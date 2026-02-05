#!/usr/bin/env python3
"""
Complete conversion script for model-slr.qmd to PreTeXt format
Handles all 1844 lines with full coverage
"""

import re
import sys
from typing import List, Tuple, Optional

class QmdToPreTeXtConverter:
    def __init__(self):
        self.lines = []
        self.output = []
        self.i = 0
        self.section_stack = []  # Track open sections/subsections
        self.in_code_block = False
        self.in_content_visible = False
        self.content_visible_depth = 0
        
    def convert_file(self, input_file: str, output_file: str):
        """Main conversion function"""
        with open(input_file, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()
        
        self.output = []
        self.i = 0
        
        # Add XML declaration and chapter opening
        self.output.append('<?xml version="1.0" encoding="UTF-8"?>')
        self.output.append('<section xml:id="sec-model-slr" xmlns:xi="http://www.w3.org/2001/XInclude">')
        self.output.append('')
        
        # Process all lines
        while self.i < len(self.lines):
            self.process_line()
            self.i += 1
        
        # Close any remaining sections
        while self.section_stack:
            tag = self.section_stack.pop()
            self.output.append(f'</{tag}>')
            self.output.append('')
        
        # Close main section
        self.output.append('</section>')
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.output))
        
        print(f"Conversion complete: {len(self.lines)} lines processed")
        print(f"Output written to: {output_file}")
    
    def current_line(self) -> str:
        """Get current line"""
        if self.i < len(self.lines):
            return self.lines[self.i].rstrip()
        return ""
    
    def peek_line(self, offset: int = 1) -> str:
        """Peek at future line"""
        idx = self.i + offset
        if idx < len(self.lines):
            return self.lines[idx].rstrip()
        return ""
    
    def process_line(self):
        """Process a single line"""
        line = self.current_line()
        
        # Skip empty lines in certain contexts
        if not line.strip():
            if not self.in_code_block:
                self.output.append('')
            return
        
        # Check for content-visible blocks (skip entirely)
        if '::: {.content-visible' in line:
            self.in_content_visible = True
            self.content_visible_depth = 1
            return
        
        if self.in_content_visible:
            if line.strip().startswith(':::'):
                if '{' in line:
                    self.content_visible_depth += 1
                else:
                    self.content_visible_depth -= 1
                    if self.content_visible_depth == 0:
                        self.in_content_visible = False
            return
        
        # Skip vspace, clearpage, footnotes
        if (line.strip().startswith(r'\vspace') or 
            line.strip().startswith(r'\clearpage') or
            line.strip().startswith('[^')):
            return
        
        # Check for display math blocks
        if line.strip() == '$$':
            self.process_display_math()
            return
        
        # Process code blocks
        if line.strip().startswith('```'):
            self.process_code_block()
            return
        
        # Process headers
        if line.startswith('#') and not line.startswith('#|'):
            self.process_header(line)
            return
        
        # Process special blocks
        if line.strip().startswith(':::'):
            self.process_special_block(line)
            return
        
        # Process includes
        if '{{< include' in line:
            self.process_include(line)
            return
        
        # Process lists
        if line.strip().startswith(('- ', '* ', '+ ')) or re.match(r'^\d+\.\s', line.strip()):
            self.process_list()
            return
        
        # Regular paragraph
        if line.strip():
            self.process_paragraph(line)
    
    def process_header(self, line: str):
        """Process markdown headers"""
        # Extract level and content
        match = re.match(r'^(#{1,4})\s+(.+?)(?:\s+\{#([^}]+)\})?$', line)
        if not match:
            return
        
        hashes, title, xml_id = match.groups()
        level = len(hashes)
        
        # Clean title
        title = self.convert_inline(title)
        
        # Close sections as needed
        if level == 1:
            # Close all sections
            while self.section_stack:
                tag = self.section_stack.pop()
                self.output.append(f'</{tag}>')
                self.output.append('')
            # This is the main title
            self.output.append(f'<title>{title}</title>')
            self.output.append('')
        elif level == 2:
            # Close subsections, keep sections
            while self.section_stack and self.section_stack[-1] == 'subsection':
                tag = self.section_stack.pop()
                self.output.append(f'</{tag}>')
                self.output.append('')
            # Close previous section if any
            if self.section_stack and self.section_stack[-1] == 'section':
                tag = self.section_stack.pop()
                self.output.append(f'</{tag}>')
                self.output.append('')
            # Open new section
            if xml_id:
                self.output.append(f'<section xml:id="{xml_id}">')
            else:
                self.output.append('<section>')
            self.output.append(f'  <title>{title}</title>')
            self.output.append('')
            self.section_stack.append('section')
        elif level == 3:
            # Close previous subsection if any
            if self.section_stack and self.section_stack[-1] == 'subsection':
                tag = self.section_stack.pop()
                self.output.append(f'</{tag}>')
                self.output.append('')
            # Open new subsection
            if xml_id:
                self.output.append(f'<subsection xml:id="{xml_id}">')
            else:
                self.output.append('<subsection>')
            self.output.append(f'  <title>{title}</title>')
            self.output.append('')
            self.section_stack.append('subsection')
    
    def process_code_block(self):
        """Process R code blocks"""
        start_line = self.i
        self.i += 1
        
        # Collect metadata and code
        metadata = {}
        code_lines = []
        current_key = None
        
        while self.i < len(self.lines):
            line = self.current_line()
            if line.strip().startswith('```'):
                break
            
            # Check for metadata
            if line.strip().startswith('#|'):
                content = line.strip()[2:].strip()
                if ':' in content:
                    parts = content.split(':', 1)
                    key = parts[0].strip()
                    value = parts[1].strip()
                    current_key = key
                    if key in metadata:
                        metadata[key] += ' ' + value
                    else:
                        metadata[key] = value
                else:
                    # Continuation of previous metadata
                    if current_key and current_key in metadata:
                        metadata[current_key] += ' ' + content
            else:
                code_lines.append(line)
            
            self.i += 1
        
        # Determine what to do with this code block
        label = metadata.get('label', '')
        include = metadata.get('include', 'true')
        
        # Skip if include: false or if it's terms assignment
        if include == 'false':
            return
        
        code_text = '\n'.join(code_lines).strip()
        if 'terms_chp_' in code_text and '=' in code_text:
            return
        
        # Check if this is a figure
        if label.startswith('fig-'):
            fig_cap = metadata.get('fig-cap', '')
            fig_cap = fig_cap.strip('|').strip()
            fig_cap = self.convert_inline(fig_cap)
            
            self.output.append(f'<figure xml:id="{label}">')
            self.output.append(f'  <caption>{fig_cap}</caption>')
            self.output.append(f'  <image source="images/{label}-1.png" width="70%" />')
            self.output.append('</figure>')
            self.output.append('')
        
        # Check if this is a table
        elif label.startswith('tbl-'):
            tbl_cap = metadata.get('tbl-cap', '')
            tbl_cap = tbl_cap.strip('|').strip()
            tbl_cap = self.convert_inline(tbl_cap)
            
            self.output.append(f'<figure xml:id="{label}">')
            self.output.append(f'  <caption>{tbl_cap}</caption>')
            self.output.append(f'  <image source="images/{label}-1.png" width="70%" />')
            self.output.append('</figure>')
            self.output.append('')
        
        # Otherwise, code blocks with labels but no figures/tables are skipped
        # (they're usually for data prep, plot theme setup, etc.)
        # Code blocks with no label at all are also skipped (they're minimal/setup)
    
    def process_special_block(self, line: str):
        """Process special blocks like guidedpractice, workedexample, etc."""
        # Determine block type
        if '.guidedpractice' in line:
            self.process_guided_practice()
        elif '.workedexample' in line:
            self.process_worked_example()
        elif '.data' in line:
            self.process_data_block()
        elif '.important' in line:
            self.process_important_block()
        elif '.pronunciation' in line:
            # Skip pronunciation blocks (they're in content-visible)
            self.skip_until_closing_fence()
        elif '.chapterintro' in line:
            self.process_chapterintro()
        else:
            # Generic block, skip
            self.skip_until_closing_fence()
    
    def process_chapterintro(self):
        """Process chapter introduction"""
        self.i += 1
        content_lines = []
        
        while self.i < len(self.lines):
            line = self.current_line()
            if line.strip() == ':::':
                break
            if line.strip():
                content_lines.append(line)
            self.i += 1
        
        # Output as introduction
        self.output.append('<introduction>')
        for line in content_lines:
            if line.strip():
                converted = self.convert_inline(line.strip())
                self.output.append(f'  <p>{converted}</p>')
        self.output.append('</introduction>')
        self.output.append('')
    
    def process_guided_practice(self):
        """Process guided practice (exercise with solution)"""
        self.i += 1
        statement_lines = []
        solution_lines = []
        in_solution = False
        in_callout = False
        
        while self.i < len(self.lines):
            line = self.current_line()
            
            if line.strip() == ':::' and not in_callout:
                break
            
            if '::: {.callout-note' in line:
                in_callout = True
                self.i += 1
                continue
            
            if in_callout and line.strip() == ':::':
                in_callout = False
                self.i += 1
                continue
            
            if line.strip().startswith('## Solution'):
                in_solution = True
                self.i += 1
                continue
            
            if in_solution:
                if line.strip():
                    solution_lines.append(line)
            else:
                if line.strip():
                    statement_lines.append(line)
            
            self.i += 1
        
        # Output exercise
        self.output.append('<exercise>')
        self.output.append('  <statement>')
        for line in statement_lines:
            if line.strip():
                converted = self.convert_inline(line.strip())
                self.output.append(f'    <p>{converted}</p>')
        self.output.append('  </statement>')
        
        if solution_lines:
            self.output.append('  <solution>')
            for line in solution_lines:
                if line.strip():
                    converted = self.convert_inline(line.strip())
                    self.output.append(f'    <p>{converted}</p>')
            self.output.append('  </solution>')
        
        self.output.append('</exercise>')
        self.output.append('')
    
    def process_worked_example(self):
        """Process worked example"""
        self.i += 1
        statement_lines = []
        solution_lines = []
        in_solution = False
        
        while self.i < len(self.lines):
            line = self.current_line()
            
            if line.strip() == ':::':
                break
            
            # Check for separator
            if re.match(r'^-{3,}$', line.strip()):
                in_solution = True
                self.i += 1
                continue
            
            if in_solution:
                if line.strip():
                    solution_lines.append(line)
            else:
                if line.strip():
                    statement_lines.append(line)
            
            self.i += 1
        
        # Output example
        self.output.append('<example>')
        self.output.append('  <statement>')
        for line in statement_lines:
            if line.strip():
                converted = self.convert_inline(line.strip())
                self.output.append(f'    <p>{converted}</p>')
        self.output.append('  </statement>')
        
        if solution_lines:
            self.output.append('  <solution>')
            for line in solution_lines:
                if line.strip():
                    converted = self.convert_inline(line.strip())
                    self.output.append(f'    <p>{converted}</p>')
            self.output.append('  </solution>')
        
        self.output.append('</example>')
        self.output.append('')
    
    def process_data_block(self):
        """Process data block"""
        self.i += 1
        lines_to_process = []
        
        while self.i < len(self.lines):
            line = self.current_line()
            if line.strip() == ':::':
                break
            lines_to_process.append(line)
            self.i += 1
        
        self.output.append('<note>')
        self.output.append('  <title>Data</title>')
        
        for line in lines_to_process:
            if line.strip():
                converted = self.convert_inline(line.strip())
                self.output.append(f'  <p>{converted}</p>')
        
        self.output.append('</note>')
        self.output.append('')
    
    def process_important_block(self):
        """Process important block"""
        self.i += 1
        lines_to_process = []
        
        while self.i < len(self.lines):
            line = self.current_line()
            if line.strip() == ':::':
                break
            lines_to_process.append(line)
            self.i += 1
        
        self.output.append('<assemblage>')
        
        # Process lines inside assemblage
        j = 0
        while j < len(lines_to_process):
            line = lines_to_process[j].strip()
            
            if not line:
                j += 1
                continue
            
            # Check for display math
            if line == '$$':
                # Find closing $$
                j += 1
                math_lines = []
                while j < len(lines_to_process) and lines_to_process[j].strip() != '$$':
                    math_lines.append(lines_to_process[j].strip())
                    j += 1
                j += 1  # Skip closing $$
                
                math_content = ' '.join(math_lines)
                if len([l for l in math_lines if l.strip()]) > 1 or '\\\\' in math_content:
                    self.output.append('  <md>')
                    for mline in math_lines:
                        if mline.strip():
                            self.output.append(f'    <mrow>{mline.strip()}</mrow>')
                    self.output.append('  </md>')
                else:
                    self.output.append(f'  <me>{math_content}</me>')
            else:
                converted = self.convert_inline(line)
                self.output.append(f'  <p>{converted}</p>')
                j += 1
        
        self.output.append('</assemblage>')
        self.output.append('')
    
    def skip_until_closing_fence(self):
        """Skip until closing ::: """
        depth = 1
        self.i += 1
        
        while self.i < len(self.lines) and depth > 0:
            line = self.current_line()
            if line.strip().startswith(':::'):
                if '{' in line:
                    depth += 1
                else:
                    depth -= 1
            self.i += 1
        self.i -= 1
    
    def process_display_math(self):
        """Process display math blocks $$...$$ """
        self.i += 1
        math_lines = []
        
        while self.i < len(self.lines):
            line = self.current_line()
            if line.strip() == '$$':
                break
            math_lines.append(line.strip())
            self.i += 1
        
        # Combine math lines
        math_content = ' '.join(math_lines)
        
        # Check if multi-line (has \\ or multiple non-empty lines)
        if len([l for l in math_lines if l.strip()]) > 1 or '\\\\' in math_content:
            # Use <md> for multi-line
            self.output.append('<md>')
            for line in math_lines:
                if line.strip():
                    self.output.append(f'  <mrow>{line.strip()}</mrow>')
            self.output.append('</md>')
        else:
            # Use <me> for single line
            self.output.append(f'<me>{math_content}</me>')
        
        self.output.append('')
    
    def process_list(self):
        """Process bulleted or ordered lists"""
        items = []
        is_ordered = re.match(r'^\d+\.\s', self.current_line().strip())
        
        while self.i < len(self.lines):
            line = self.current_line()
            
            # Check if still in list
            if not line.strip():
                # Empty line might mean end of list, check next
                next_line = self.peek_line()
                if next_line.strip() and not next_line.strip().startswith(('- ', '* ', '+ ')) and not re.match(r'^\d+\.\s', next_line.strip()):
                    break
                self.i += 1
                continue
            
            # Check for list item
            match = re.match(r'^[-*+]\s+(.+)', line.strip())
            if not match and not is_ordered:
                break
            
            if is_ordered:
                match = re.match(r'^\d+\.\s+(.+)', line.strip())
                if not match:
                    break
            
            item_text = match.group(1)
            items.append(item_text)
            self.i += 1
        
        # Don't increment again at end
        self.i -= 1
        
        # Output list
        list_tag = 'ol' if is_ordered else 'ul'
        self.output.append(f'<{list_tag}>')
        for item in items:
            converted = self.convert_inline(item)
            self.output.append(f'  <li><p>{converted}</p></li>')
        self.output.append(f'</{list_tag}>')
        self.output.append('')
    
    def process_include(self, line: str):
        """Process include statements"""
        match = re.search(r'{{<\s*include\s+([^>]+)\s*>}}', line)
        if match:
            path = match.group(1).strip()
            # Convert .qmd to .ptx
            path = path.replace('.qmd', '.ptx')
            self.output.append(f'<xi:include href="{path}" />')
            self.output.append('')
    
    def process_paragraph(self, line: str):
        """Process regular paragraph"""
        # Convert inline elements
        converted = self.convert_inline(line.strip())
        if converted:
            self.output.append(f'<p>{converted}</p>')
            self.output.append('')
    
    def convert_inline(self, text: str) -> str:
        """Convert inline markdown to PreTeXt"""
        # Keep index markers
        # text already has \index{...}
        
        # Convert cross-references @fig-ref, @tbl-ref, @sec-ref
        text = re.sub(r'@(fig-[a-zA-Z0-9_-]+)', r'<xref ref="\1" />', text)
        text = re.sub(r'@(tbl-[a-zA-Z0-9_-]+)', r'<xref ref="\1" />', text)
        text = re.sub(r'@(sec-[a-zA-Z0-9_-]+)', r'<xref ref="\1" />', text)
        
        # Convert links [text](url)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<url href="\2">\1</url>', text)
        
        # Convert display math $$ ... $$
        # Handle multi-line later, for now single line
        text = re.sub(r'\$\$([^$]+)\$\$', r'<me>\1</me>', text)
        
        # Convert inline math $ ... $
        text = re.sub(r'\$([^$]+)\$', r'<m>\1</m>', text)
        
        # Convert inline code ` ... `
        text = re.sub(r'`([^`]+)`', r'<c>\1</c>', text)
        
        # Convert bold **text**
        text = re.sub(r'\*\*([^*]+)\*\*', r'<alert>\1</alert>', text)
        
        # Convert italic *text* (but not already converted **)
        text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
        
        return text

def main():
    converter = QmdToPreTeXtConverter()
    converter.convert_file(
        '/home/runner/work/ims/ims/model-slr.qmd',
        '/home/runner/work/ims/ims/source/chapters/ch07-linear-regression-single.ptx'
    )

if __name__ == '__main__':
    main()
