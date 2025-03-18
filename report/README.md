# Artificial Intelligence

Artificial Intelligence Class Report

#Latex Requirements

1. Install LaTeX Distribution
   Windows: Download and install MikTeX or TeX Live.
   MikTeX allows you to install packages on the fly, which is useful for beginners.
   TeX Live provides a more complete setup but is larger in size.
   macOS: Install MacTeX, which includes TeX Live.
   Linux: Install TeX Live via the terminal

2. Install LaTeX Workshop Extension on Vscode
   Open VS Code.
   Go to the Extensions view by clicking on the Extensions icon on the Activity Bar or pressing Ctrl+Shift+X.
   Search for LaTeX Workshop and install it. This extension provides LaTeX support, compilation, previews, and syntax highlighting.
3. Configure LaTeX Workshop
   Once installed, LaTeX Workshop will automatically configure itself to use the default LaTeX distribution on your system. However, you may need to adjust settings if you have a custom setup.

Open Settings: Go to File > Preferences > Settings.
Search for LaTeX Workshop settings and configure paths if necessary:
For example, if you're on macOS, make sure your path includes /Library/TeX/texbin if using MacTeX.
Optional: Adjust compilation commands in .vscode/settings.json for specific preferences, such as:

{
"latex-workshop.latex.tools": [
{
"name": "pdflatex",
"command": "pdflatex",
"args": ["-synctex=1", "-interaction=nonstopmode", "-file-line-error", "%DOC%"]
},
{
"name": "latexmk",
"command": "latexmk",
"args": ["-synctex=1", "-interaction=nonstopmode", "-file-line-error", "-pdf", "%DOC%"]
}
],
"latex-workshop.latex.recipes": [
{
"name": "latexmk 🔄",
"tools": ["latexmk"]
}
]
}

4. Compile Your Document
   Open a .tex file in VS Code.
   Use Ctrl+Alt+B (or Cmd+Option+B on macOS) to compile your document.
   LaTeX Workshop will use the default recipe, typically latexmk, to compile the .tex file into a PDF.
   View the PDF output in the LaTeX Workshop PDF viewer (usually on the right side of VS Code).
