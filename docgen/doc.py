import subprocess
from PyPDF2 import PdfReader, PdfWriter
import anthropic
import os
import sys

def generate_content_with_llm(content):
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )
    PROMPT = r"""
You are tasked with creating syntactically correct LaTeX code for a document for rez0corp. Your output should be only the LaTeX code, without any additional explanations or comments.
The LaTeX code must be compatible with pdflatex (do not use packages like fontspec that require XeLaTeX or LuaLaTeX).
Use monospace font, if you can do the section headings in thin monospace, that would be best. Use large margins (1.5 inch on all sides) for the document layout.

Here are the company details and color scheme to use:
Company Name: rez0corp
Services: Cybersecurity Services, AI Services (only mention whichever one is relevant or both if both are relevant)
Main Color: Blue (#4B77D1)
Contact Email: contact@rez0corp.com
Additional Colors: White, Black

The {SPECIFIC_CONTENT} variable will contain additional details or sections to be included in the document. Incorporate this content appropriately within the LaTeX structure.

Begin your LaTeX document with the necessary preamble, including required packages such as:
\documentclass{{article}}
\usepackage{{geometry}}
\usepackage{{xcolor}}
\usepackage{{graphicx}}
\usepackage{{titlesec}}
\usepackage{{enumitem}}

Define the company's blue color:
\definecolor{{rezoBlue}}{{HTML}}{{4B77D1}}
Don't make the main section header blue, but subsections are fine to be blue if you want. 

The section headings should be centered and large. Subsections should be left aligned.

Use appropriate sectioning commands (\section, \subsection) to structure the content. Apply the company's color scheme using \color{{rezoBlue}} for headings and important text.

For the document layout, use the geometry package to set appropriate margins:
\geometry{{margin=1in}}

Style section headings using titlesec:
\titleformat{{\section}}{{\color{{rezoBlue}}\Large\bfseries}}{{\thesection}}{{1em}}{{}}

The company logo is already at the top of a document that will be merged with this one so dont reference a logo at all (nor use a title section). And the background page is white so use black text (or blue text for cool variety in the text if you want).

For single-page documents (like proposals), do NOT use page numbers or headers/footers. ie, use: (\pagenumbering{{empty}})

Bold important terms or phrases within the text. Use bullet points for lists. Sometimes the lists you make render as {{ character and i don't like that. If you can avoid that, that would be great.

Do NOT number the sections or subsections. (you can do this by appending an asterisk to the section command, e.g., \section*{{example}}) and \subsection*{{example}}.

Do NOT use utf8 encoding. T1 seems to work well.

Don't put some cheeky slogan at the bottom. 

Output only the LaTeX code, starting with \documentclass and ending with \end{{document}}. Do not include any explanations or comments outside of the LaTeX code.
    """
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2000,
        temperature=.7,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": PROMPT.format(SPECIFIC_CONTENT=content)
                    }
                ]
            }
        ]
    )
    return message.content[0].text

def create_content_pdf(latex_content):
    # Write the LaTeX content to a file
    with open("content.tex", "w") as f:
        print(latex_content)
        f.write(latex_content)
    
    # Compile the LaTeX file to PDF
    subprocess.run(["pdflatex","-interaction=nonstopmode", "content.tex"])

def merge_pdfs(background_pdf, content_pdf, output_pdf):
    background = PdfReader(background_pdf)
    content = PdfReader(content_pdf)
    
    output = PdfWriter()
    
    # Assume both PDFs have only one page for simplicity
    page = background.pages[0]
    page.merge_page(content.pages[0])
    output.add_page(page)
    
    with open(output_pdf, "wb") as f:
        output.write(f)

def main():
    content = sys.stdin.read().strip()

    # Generate LaTeX content
    # latex_content = generate_content_with_llm("proposal for ai consulting services. prices are 5k for async only. 10k for 4 meetings and async. or variable higher pricing for more")
    latex_content = generate_content_with_llm(content)
    
    # Create a PDF with the content
    create_content_pdf(latex_content)
    
    # Merge the background and content PDFs
    merge_pdfs("background3.pdf", "content.pdf", "final_output.pdf")

    # Clean up temporary files
    for file in ['content.aux', 'content.log', 'content.pdf']:
        if os.path.exists(file):
            os.remove(file)

if __name__ == "__main__":
    main()