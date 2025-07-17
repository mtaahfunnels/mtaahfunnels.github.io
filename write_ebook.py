# write_ebook.py
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

filename = "ebooks/overwhelmed-with-tasks.pdf"

content = """
Overwhelmed With Tasks?
=======================

If you're drowning in tools, tabs, and to-do lists — you're not alone.

This short guide shows you how to eliminate distraction, simplify your workflow,
and let AI handle the boring stuff.

Inside, you'll learn:

✔️ How to audit your current tool stack  
✔️ The 3 "stack traps" that waste your time  
✔️ 5 tools that automate 80% of your tasks

You don’t need to work harder. Just smarter.
"""

c = canvas.Canvas(filename, pagesize=LETTER)
text = c.beginText(40, 750)
text.setFont("Helvetica", 12)

for line in content.strip().splitlines():
    text.textLine(line)

c.drawText(text)
c.save()
