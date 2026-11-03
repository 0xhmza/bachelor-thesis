%% bossthesis.cls
%% Copyright (C) 2021-2022 Christian Eichler <christian.eichler@rub.de>
%% Copyright (C) 2009-2011 Christoph Sommer <christoph.sommer@informatik.uni-erlangen.de>
%%                         Falko Dressler

%
% License (pick one or both):
% - Creative Commons Attribution-Share Alike 3.0 (or later)
% - GPL v2 (or later)
%
% Adapted for this thesis (26 October 2026), from the template at
% https://ai.ini.rub.de/de/studierende/planung-des-studiums/abschlussarbeiten :
% - bibliography with Biber and numeric citations (the repository builds with Biber);
% - \paragraph kept as a run-in heading instead of being renamed;
% - English title page for the Max Planck Institute for Security and Privacy
%   (MPI-SP), with \institute, \instituteaddress and \examiners in place of the
%   BOSS group and its professor;
% - declaration and AI-tools box unchanged (faculty-wide wording);
% - packages the thesis does not use removed: siunitx, acronym, algorithm,
%   algorithmic, listing, placeins, subcaption, nag;
% - todonotes without shadows (the note style is set in the thesis preamble);
% - listings without [savemem], which suppressed keyword styles;
% - the declaration box kept inside the text block;
% - no negative space above displayed equations.

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{bossthesis}[2026/10/26 The BOSS Thesis Class, adapted for MPI-SP]  % YYYY/MM/DD


% -----------------------------------------------------------------------------
% Class options
% -----------------------------------------------------------------------------
\RequirePackage{ifthen}
\RequirePackage{iftex}


% [germanthesis] - Thesis is written in German
\newboolean{germanthesis}
\setboolean{germanthesis}{false}
\DeclareOption{germanthesis}{\setboolean{germanthesis}{true}}

% [plainunnumbered] - Don't print numbers on plain pages
\newboolean{plainunnumbered}
\setboolean{plainunnumbered}{false}
\DeclareOption{plainunnumbered}{\setboolean{plainunnumbered}{true}}

% [earlydraft] - Settings for quick draft printouts
\newboolean{earlydraft}
\setboolean{earlydraft}{false}
\DeclareOption{earlydraft}{\setboolean{earlydraft}{true}}

% [watermark] - Print current time/date at bottom of each page
\newboolean{watermark}
\setboolean{watermark}{false}
\DeclareOption{watermark}{\setboolean{watermark}{true}}

% [phdthesis] - switch to PhD thesis style
\newboolean{phdthesis}
\setboolean{phdthesis}{false}
\DeclareOption{phdthesis}{\setboolean{phdthesis}{true}}

% [modernchapter] - modern chapter marks
\newboolean{modernchapter}
\setboolean{modernchapter}{false}
\DeclareOption{modernchapter}{\setboolean{modernchapter}{true}}

% [moderntitle] - modern title page
\newboolean{moderntitle}
\setboolean{moderntitle}{false}
\DeclareOption{moderntitle}{\setboolean{moderntitle}{true}}



% [twoside] - double sided
\newboolean{oneside}
\setboolean{oneside}{true}
\DeclareOption{twoside}{\setboolean{oneside}{false}}

% [privacy] - Generate a more privacy aware pdf
\newboolean{privacy}
\setboolean{privacy}{false}
\DeclareOption{privacy}{\setboolean{privacy}{true}}

\newboolean{gnuplot}
\setboolean{gnuplot}{false}
\DeclareOption{gnuplot}{\setboolean{gnuplot}{true}}


% [inf] - study subject 'Informatik'
\newboolean{studinf}
\setboolean{studinf}{false}
\DeclareOption{inf}{\setboolean{studinf}{true} }

% [ai] - study subject 'Angewandte Informatik'
\newboolean{studai}
\setboolean{studai}{false}
\DeclareOption{ai} {%
	\setboolean{studai}{true}%
	\ifthenelse{\boolean{studinf}}{\ClassError{bossthesis}{Please specify only one study subject}{}}{}
}

% [its] - study subject 'IT Security'
\newboolean{studits}
\setboolean{studits}{false}
\DeclareOption{its}{%
	\setboolean{studits}{true}
	\ifthenelse{\boolean{studinf} \OR \boolean{studai}}{\ClassError{bossthesis}{Please specify only one study subject}{}}{}
}

% [project] - study project report
\newboolean{project}
\setboolean{project}{false}
\DeclareOption{project}{\setboolean{project}{true}}

\ProcessOptions \relax
% -----------------------------------------------------------------------------


%
\ifthenelse{%
	\(\NOT\boolean{studinf}\) \AND \(\NOT\boolean{studai}\) \AND \(\NOT\boolean{studits}\)
}{\ClassError{bossthesis}{Missing class option 'study subject' - please specify one of inf, ai, or its}{}}{}
%


% -----------------------------------------------------------------------------
% Basics
% -----------------------------------------------------------------------------
% This class is based on report
\ifthenelse{\boolean{oneside}}{
\LoadClass[a4paper,10pt,onecolumn,oneside,openright]{report}
\RequirePackage[a4paper,textwidth=410pt,textheight=598pt,bindingoffset=0cm,marginparwidth=3cm,hmarginratio=1:1,vmarginratio=1:1]{geometry}
}{
\LoadClass[a4paper,10pt,onecolumn,twoside,openright]{report}
\RequirePackage[a4paper,textwidth=410pt,textheight=598pt,bindingoffset=0cm,marginparwidth=3cm,hmarginratio=1:1,vmarginratio=1:1]{geometry}
}
\setlength\parskip{0pt} 

% 150 percent line spacing
\RequirePackage{setspace}

% Allow more (and larger) floats on text pages
\renewcommand{\topfraction}{0.9}  % use up to ..% of space on top
\renewcommand{\bottomfraction}{0.8}  % use up to ..% of space on bottom
\setcounter{topnumber}{4} % place up to .. on top
\setcounter{bottomnumber}{1} % place up to .. on bottom
\setcounter{totalnumber}{4} % place up to .. total
\renewcommand{\textfraction}{0.07} % allow down to ..% of text
\renewcommand{\floatpagefraction}{0.7} % fill at least ..% of float pages (must be less than \topfraction)

% Avoid widows and orphans (single line on bottom or top of page, respectively) at almost any cost
\clubpenalty = 10000
\widowpenalty = 10000
\displaywidowpenalty = 10000 % formulas
%\raggedbottom

% Default fonts
\newcommand{\mypageheadfont}{\normalfont}
\newcommand{\myheadingfont}{\normalfont}
%\RequirePackage[osf]{libertine}  % Linux Libertine
%\renewcommand{\mypageheadfont}{\normalfont\libertine}
%\renewcommand{\myheadingfont}{\normalfont\libertine}
\IfFileExists{XCharter}{
\RequirePackage[sups,scaled=.98]{XCharter}
\RequirePackage[charter,bigdelims,vvarbb,scaled=1.07]{newtxmath}
\RequirePackage[cal=boondoxo]{mathalfa}
}{
\RequirePackage[bitstream-charter,sfscaled=false]{mathdesign}  % RM: Bitstream Charter
}
\RequirePackage{helvet}  % SF: Helvetica 
\RequirePackage[scaled=1.04,varqu,varl]{inconsolata} % TT: Inconsolata
\linespread{1.04}
% TODO: nicer math font?

% More encoding and typesetting fixes and tweaks
\ifPDFTeX
\RequirePackage[utf8]{inputenc}
\fi
\RequirePackage[T1]{fontenc}
\RequirePackage{textcomp}
\ifthenelse{\boolean{earlydraft}}{
	\newcommand{\mydisableprotrusion}{}
    \newcommand{\textls}[2][]{#2}
}{
  \ifPDFTeX
     \RequirePackage[babel,protrusion=true,expansion=true,tracking=false,kerning=true,spacing=true]{microtype}
  \else
     \RequirePackage[babel,protrusion=true,expansion=true,tracking=false,kerning=false,spacing=false]{microtype}
  \fi
  \newcommand{\mydisableprotrusion}{\microtypesetup{protrusion=false}}
}
\RequirePackage{hyphenat}

% Graphics insertion and filetypes' order of precedence
\ifPDFTeX
\RequirePackage[pdftex]{graphicx}
\pdfminorversion=6
\else
\RequirePackage{graphicx}
\fi
\DeclareGraphicsRule{.out.png}{png}{.out.png}{}
\ifthenelse{\boolean{earlydraft}}{
	\DeclareGraphicsExtensions{.thumb.jpg,.out.png,.pdf,.png,.jpg}
	\DeclareGraphicsRule{.thumb.jpg}{jpg}{.thumb.jpg}{}
}{
	\DeclareGraphicsExtensions{.out.png,.pdf,.png,.jpg}
}

% Typesetting URLs
\RequirePackage[lowtilde]{url}
\urlstyle{tt}

% For hyperref<->algorithm interaction
\RequirePackage{float}

% Cross-references are clickable
\RequirePackage[pdftex,
                bookmarks=true,
                bookmarksnumbered=true,
                colorlinks=false,
                pdfdisplaydoctitle=true,
                breaklinks=true]{hyperref}
% Link to beginning of floats
\RequirePackage[all]{hypcap}

% Captions
\RequirePackage[font=small, labelfont=bf, labelsep=endash, margin=1cm]{caption}

% Citations
\RequirePackage[backend=biber,style=numeric-comp,sorting=nyt,maxbibnames=99,urldate=long]{biblatex}
\defbibheading{bibliography}[\refname]{\chapter*{#1}\chaptermark{#1}}

% Commands for beautiful tables
\RequirePackage{booktabs}

% Equation typesetting fixes and tweaks + proof/theorem environment
\RequirePackage{amsmath}
\newtheorem{thm}{Theorem}[section]
% The template set the space above displays to -0.5em, which made tall
% displays (cases, fractions) overlap the line before them; the standard
% skips of the report class are kept instead.

% -----------------------------------------------------------------------------


% -----------------------------------------------------------------------------
% Internationalization support
% -----------------------------------------------------------------------------

% Multi-language support using Babel
\ifthenelse{\boolean{germanthesis}}{
	\RequirePackage[american,ngerman]{babel}
    \def\cvtitle{Lebenslauf}
}{
	\RequirePackage[ngerman,american]{babel}
    \def\cvtitle{Curriculum Vitae}
}

% Time and date functions
\RequirePackage{datetime}

% Clever References
\ifthenelse{\boolean{germanthesis}}{
	\RequirePackage[ngerman]{cleveref}[2009/17/04]
	\def\cref{\Cref}
	\def\crefrange{\Crefrange}
	\crefname{lstlisting}{Listing}{Listings}
	\Crefname{lstlisting}{Listing}{Listings}
	\crefname{listing}{Listing}{Listings}
	\Crefname{listing}{Listing}{Listings}
	\crefname{algorithm}{Algorithmus}{Algorithmen}
	\Crefname{algorithm}{Algorithmus}{Algorithmen}
}{
	\RequirePackage{cleveref}[2009/17/04]
	\def\cref{\Cref}
	\def\crefrange{\Crefrange}
	\crefname{lstlisting}{listing}{listings}
	\Crefname{lstlisting}{Listing}{Listings}
	\crefname{listing}{listing}{listings}
	\Crefname{listing}{Listing}{Listings}
	\crefname{algorithm}{algorithm}{algorithms}
	\Crefname{algorithm}{Algorithm}{Algorithms}
}

% Some more language-dependent commands
\ifthenelse{\boolean{germanthesis}}{
	\newcommand{\thedate}{\today}
	\newcommand{\glossarytitlename}{Abkürzungsverzeichnis}
    \newcommand{\listoftitlename}{Verzeichnisse}
}{
  \RequirePackage[german,american]{isodate}
  \newcommand{\thedate}{
    \makeatletter
    \def\iso@languagename{german}%
    \dategerman%
    \today
    \def\iso@languagename{american}%
    \makeatother
  }
  \newcommand{\listoftitlename}{Lists}
  \newcommand{\glossarytitlename}{List of Acronyms}
}

% Language-independent timestamp
\newcommand{\timestamp}{\renewcommand{\dateseparator}{-}\yyyymmdddate\today\quad\settimeformat{hhmmsstime}\currenttime}

% -----------------------------------------------------------------------------


% -----------------------------------------------------------------------------
% All the simple stuff goes here
% -----------------------------------------------------------------------------

% Make automatically inserted "blank pages" really blank
\RequirePackage{emptypage}

% Fix spacing around "..."
\RequirePackage{ellipsis}

% TeX ist kein Zeichenprogramm
\RequirePackage{tikz}[2010/10/13]
\usetikzlibrary{patterns}

% Sans Serif Font for tikzpictures
\tikzset{every picture/.append style={font=\sffamily}}

\ifthenelse{\boolean{gnuplot}}{
\RequirePackage{pgf}
\RequirePackage{pgfplots}
\RequirePackage{pgfplotstable}
\pgfplotsset{compat=newest}
\RequirePackage{gnuplot/gnuplot-lua-tikz}
\usetikzlibrary{external}
\tikzexternalize[prefix=generated/]
\tikzset{external/export=false}
% reduce distance between float and description
%\renewcommand{\floatpagefraction}{.97}
%\addtolength{\abovecaptionskip}{-.9em}
\newlength{\gnuplotcaptionskip}
%\setlength{\gnuplotcaptionskip}{-2.2em}
\newlength{\gnuplotundercaptionskip}
\setlength{\gnuplotundercaptionskip}{-1em}
\newlength{\gnuplotpreskip}
\addtolength{\gnuplotpreskip}{-0.5em}
\addtolength{\intextsep}{-0.1em}
\addtolength{\floatsep}{-0.1em}
\addtolength{\textfloatsep}{-0.1em}
\addtolength{\dblfloatsep}{-0.1em}
\addtolength{\dbltextfloatsep}{-0.1em}
\addtolength{\topsep}{-2ex}
}{}


% This removes the auto anchor feature, when an explicit anchor is given
\tikzset{anchor/.append code={\let\tikz@auto@anchor\relax\let\tikz@compute@direction\pgfutil@gobble}}

% Ensure that no floats are typeset before they are referenced
\RequirePackage{flafter}

% The template loaded nag here (warnings about deprecated commands); removed
% to save about a tenth of each pass. Lint with chktex instead.

% Define command that will return current filename
\ifthenelse{\boolean{watermark}}{
  \RequirePackage{currfile}
}{}

% Do not reset footnote counter on new chapter
\RequirePackage[]{chngcntr}
\counterwithout{footnote}{chapter}

% "Draft" watermark
\newcommand{\thewatermark}{\ifthenelse{\boolean{watermark}}{%
	\begin{tikzpicture}[remember picture, overlay]
		\node[anchor=south, outer sep=3.75cm] at (current page.south) {
			\color{gray}\currfilename\quad\timestamp
		};
	\end{tikzpicture}%
}{}}

% Chapter/section headings and page styles
%\RequirePackage[pagestyles,nobottomtitles*]{titlesec}
\RequirePackage[pagestyles]{titlesec}
\ifthenelse{\boolean{plainunnumbered}}{
\renewpagestyle{plain}{%
	\sethead{}{}{}
	\setfoot{}{\thewatermark}{}
}
}{
\renewpagestyle{plain}{%
	\sethead{}{}{}
  \ifthenelse{\boolean{oneside}}{
    \setfoot{}{\mypageheadfont\thepage}{\thewatermark}
  }{
    \setfoot*{}{\thewatermark}{\mypageheadfont\thepage}
  }
}
}

% Pagestyle "fancy"
\newpagestyle{fancy}{ % keep in sync with fancy-lists style
  \ifthenelse{\boolean{oneside}}{
    \sethead*{
      \bfseries
      \toptitlemarks
      \mypageheadfont\bfseries
      \ifthechapter{
        \ifthesection{\thesection~\sectiontitle}{\thechapter~\chaptertitle}
      }{
        \chaptertitle
      }
    }{
    }{
    }
    \setfoot*{}{}{\thewatermark}
  }{
    \sethead*{
    }{
    }{
      \bfseries
      \toptitlemarks
      \mypageheadfont\bfseries
      \ifthechapter{
        \ifthesection{\thesection~\sectiontitle}{\thechapter~\chaptertitle}
      }{
        \chaptertitle
      }
    }
    \setfoot*{}{\thewatermark}{\mypageheadfont\thepage}
  }
  \headrule
}
\pagestyle{fancy}

% The listings at the end of the thesis use unnumbered chapters and sections.
% Therefore, a separate page style without numbers is required.  Otherwise, the
% outdated numbers would be used for all the following unnumbered chapters.
% Moreover, the use of \sectionmark{sectionname} at the beginning of each section
% is required to obtain the correct section name for the page header.
\newpagestyle{fancy-lists}{ % keep in sync with fancy style
  \ifthenelse{\boolean{oneside}}{
    \sethead*{
      \scshape
      \toptitlemarks
      \mypageheadfont\scshape
      \ifthechapter{
        \ifthesection{\sectiontitle}{\chaptertitle}
      }{
        \chaptertitle
      }
    }{
    }{
    }
    \setfoot*{}{}{\thewatermark}
  }{
    \sethead*{
    }{
    }{
      \scshape
      \toptitlemarks
      \mypageheadfont\scshape
      \ifthechapter{
        \ifthesection{\sectiontitle}{\chaptertitle}
      }{
        \chaptertitle
      }
    }
    \setfoot*{}{\thewatermark}{\mypageheadfont\thepage}
  }
  \headrule
}


% The template renamed \paragraph to \subsubsubsection; this thesis uses
% \paragraph for run-in headings, so it is kept (format below).

% heading styles
\ifthenelse{\boolean{modernchapter}}{%
  \RequirePackage{calc}
  \RequirePackage{textcase}
  \newlength{\@chapterwidth}

  \DeclareRobustCommand{\spacedallcaps}[1]{\textls[160]{\MakeTextUppercase{#1}}}

  \titleformat{\chapter}[display]%
  {\relax}% Format
  {\mbox{}\marginpar{\color{gray}\fontsize{96pt}{96pt}\selectfont%
      \setlength{\@chapterwidth}{\widthof{\thechapter}}%
      \vspace{-25pt}\hspace{-1.2\@chapterwidth}%
    \thechapter
  }}%Label
  {0pt}% Seperator
  {\vspace*{.9\baselineskip}\raggedright\huge\bfseries\spacedallcaps} %BeforeCode
  [\normalsize\titlerule]% AfterCode
}{
 \titleformat{\chapter}[display]{\myheadingfont\huge\bfseries\titlerule\vspace{0.25cm}}{\LARGE\chaptertitlename~\thechapter}{1em}{}[\vspace{0.25cm}\titlerule]
}
\titleformat{\section}{\myheadingfont\Large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\myheadingfont\large\bfseries}{\thesubsection}{1em}{}
\titleformat{\subsubsection}{\myheadingfont\normalsize\bfseries}{\thesubsubsection}{1em}{}
\titleformat{\paragraph}[runin]{\myheadingfont\normalsize\bfseries}{\theparagraph}{0pt}{}
\titleformat{\subparagraph}{\myheadingfont\normalsize}{\thesubparagraph}{1em}{\labelitemi~}
\titlespacing*{\chapter}{0pt}{50pt}{40pt}
\titlespacing*{\section}{0pt}{3.5ex plus 1ex minus .2ex}{2.3ex plus .2ex}
\titlespacing*{\subsection}{0pt}{3.25ex plus 1ex minus .2ex}{1.5ex plus .2ex}
\titlespacing*{\subsubsection}{0pt}{3.25ex plus 1ex minus .2ex}{1.5ex plus .2ex} 
\titlespacing*{\paragraph}{0pt}{1.5ex plus 1ex minus .2ex}{0.6em}
\titlespacing*{\subparagraph}{0pt}{3.25ex plus 1ex minus .2ex}{1.5ex plus .2ex} 
\ifthenelse{\boolean{earlydraft}}{
	\setcounter{tocdepth}{3}
	\setcounter{secnumdepth}{3}
}{
	\setcounter{tocdepth}{3}
	\setcounter{secnumdepth}{3}
}

% BOSS Cover Page 
\RequirePackage{bosscoverpage}
% -----------------------------------------------------------------------------


% -----------------------------------------------------------------------------
% Commands for setting author, title, ... 
% -----------------------------------------------------------------------------
\renewcommand{\author}[1]{\gdef\theauthor{#1}}
\renewcommand{\title}[1]{\gdef\thetitle{#1}}
\newcommand{\germantitle}[1]{\gdef\thegermantitle{#1}}
\newcommand{\thesistype}[1]{\gdef\thethesistype{#1}}
\newcommand{\thesiscite}[1]{\gdef\thethesiscite{#1}}
\newcommand{\birthday}[1]{\gdef\thebirthday{#1}}
\newcommand{\birthplace}[1]{\gdef\thebirthplace{#1}}
\newcommand{\thesisstart}[1]{\gdef\thethesisstart{#1}}
\newcommand{\thesisend}[1]{\gdef\thethesisend{#1}}
\newcommand{\advisors}[1]{\gdef\theadvisors{#1}}
\newcommand{\dean}[1]{\gdef\thedean{#1}}
\newcommand{\aitools}[1]{\gdef\theaitools{#1}}
\newcommand{\institute}[1]{\gdef\theinstitute{#1}}
\newcommand{\instituteaddress}[1]{\gdef\theinstituteaddress{#1}}
\newcommand{\examiners}[1]{\gdef\theexaminers{#1}} % rows of the title-page table
% -----------------------------------------------------------------------------


% -----------------------------------------------------------------------------
% Listings
% -----------------------------------------------------------------------------
\RequirePackage{listings} % without [savemem], which dropped the keyword styles
\ifthenelse{\boolean{germanthesis}}{
    \gdef\listlistingname{Quellcodeverzeichnis}
	\renewcommand{\lstlistlistingname}{Quellcodeverzeichnis}
}{
    \gdef\listlistingname{List of Listings}
	\renewcommand{\lstlistlistingname}{List of Listings}
}

% leave a gap between entries in list of listings that belong to different
% chapters so it is consistent with list of tables and figures
\let\Chapter\chapter
\def\chapter{\addtocontents{lol}{\protect\addvspace{10pt}}\Chapter}

\lstset{
	language=C,
	frame=lines,
	framesep=5pt,
	captionpos=b,
	abovecaptionskip=1em,
	numbers=left,
	xleftmargin=15pt,
	framexleftmargin=15pt,
	numberstyle=\tiny,
	numbersep=5pt,
	stepnumber=1,
	fontadjust,
	tabsize=2,
	showtabs=false,
	showspaces=false,
	showstringspaces=false,
	breaklines=true,
	breakatwhitespace=true,
	keywordstyle=\color{black},
	identifierstyle=\bfseries\color{blue},
	commentstyle=\color{red},
	prebreak=\raisebox{0ex}[0ex][0ex]{\color{gray}\ensuremath{\searrow}},
	stringstyle=\bfseries\color{blue},
	basicstyle=\ttfamily\bfseries\color{black}\footnotesize
}
\lstdefinestyle{txt}{
	float,
	language=C
}
\lstdefinestyle{xml}{
	float,
	language=XML
}
% -----------------------------------------------------------------------------


% -----------------------------------------------------------------------------
% TOCs
% -----------------------------------------------------------------------------

% Include list-of-Xs in table of contents
\ifthenelse{\boolean{earlydraft}}{
	\RequirePackage[]{tocbibind}
	\renewcommand{\lstlistoflistings}{\begingroup\tocfile{\lstlistlistingname}{lol}\endgroup}
	\newcommand{\mymakeglossarytocentry}{\addcontentsline{toc}{chapter}{\glossarytitlename}}
	\newcommand{\mymaketodotocentry}{\todototoc}
}{
	\RequirePackage[nottoc,notlot,notlof]{tocbibind}
	\newcommand{\mymakeglossarytocentry}{}
	\newcommand{\mymaketodotocentry}{}
}

% -----------------------------------------------------------------------------


% -----------------------------------------------------------------------------
% Visible TODO and FIXME markers
% -----------------------------------------------------------------------------
\ifthenelse{\boolean{germanthesis}}{
	\RequirePackage[colorinlistoftodos, textwidth=2.8cm, ngerman]{todonotes}
	\makeatletter
	\@todonotes@SetTodoListName{Offene Punkte}
	\makeatother
}{
	\RequirePackage[colorinlistoftodos, textwidth=3.0cm]{todonotes}
}
\newcounter{TODOCOUNT}
\newcommand{\TODO}[1]{\vspace{0.5em}\todo[inline, color=orange]{#1}\stepcounter{TODOCOUNT}}
\newcommand{\FIXME}[1]{\todo[size=\small, color=red]{#1}\stepcounter{TODOCOUNT}}
\AtEndDocument{
	\ifnum\value{TODOCOUNT}>0
		%\cleardoublepage
		\mymaketodotocentry\listoftodos
	\fi
}
% -----------------------------------------------------------------------------


% -----------------------------------------------------------------------------
% Title page
% -----------------------------------------------------------------------------
\renewcommand{\maketitle}{%

% Do some stuff we had to postpone until after e.g. \thetitle was set
\hypersetup{%
  pdftitle = {\thetitle},
  pdfsubject = {\thethesistype},
  pdfauthor = {\theauthor},
  pdfborder=0 0 0
}

\pagenumbering{alph}

% Output cover page
\makecoverpage

% Title pages use single line spacing, no parindent and no parskips
\begin{singlespace}
\setlength\parindent{0pt} 
\setlength\parskip{0pt} 

%
% Now output the title page
%

\pagestyle{empty}
\pagenumbering{roman}

\ifthenelse{\boolean{phdthesis}}
{
\thispagestyle{empty}

\vspace*{1.5cm}

\begin{center}
\begin{singlespace}
\LARGE
\textbf{\thetitle}\\
\vspace*{.5\baselineskip}
---\\
\vspace*{.5\baselineskip}
\textbf{\thegermantitle}\\
\end{singlespace}

\vspace*{3cm}

\begin{doublespacing}
\large
Der Fakultät für Informatik der\\
Ruhr-Universität Bochum\\
zur Erlangung des Grades\\
~\\
D\,O\,K\,T\,O\,R\,-\,I\,N\,G\,E\,N\,I\,E\,U\,R\\
~\\
vorgelegt von\\
~\\
\theauthor\\
~\\
Bochum -- \the\year\\
\end{doublespacing}
\end{center}

\clearpage

\thispagestyle{empty}

\vspace*{14cm}

\begin{center}

\begin{onehalfspacing}
Als Dissertation genehmigt von\\

der Fakultät für Informatik der\\

Ruhr-Universität Bochum\\[2\baselineskip]

\begin{tabular}{>{\raggedleft}p{5cm}p{7cm}}
Tag der Einreichung: & \textbf{\thethesisstart} \\
Tag der Promotion:   & \textbf{\thethesisend}   \\
Dekan:               & \textbf{\thedean}        \\
Berichterstatter:    \theadvisors            
\end{tabular}
\end{onehalfspacing}

\end{center}

\cleardoublepage
}
% else: Master Thesis title page
{
\thispagestyle{empty}

\vspace*{0.8cm}

\begin{center}

{\LARGE \textbf{\thetitle}}\\[2\baselineskip]

{\large
\thethesistype\\[2\baselineskip]

submitted by\\[2\baselineskip]

\textbf{\theauthor}\\[1\baselineskip]

\ifthenelse{\boolean{privacy}}{}{%
born on \thebirthday\par
in \thebirthplace\par\vspace{2\baselineskip}
}

carried out at the\\[2\baselineskip]

\textbf{\theinstitute}\\[1.2\baselineskip]
in cooperation with the\\[0.6\baselineskip]
\textbf{
Faculty of Computer Science\\[0.2\baselineskip]
Ruhr-Universität Bochum\\[0.2\baselineskip]
}
}~\\[1\baselineskip]

\begin{tabular}{>{\raggedleft}p{5cm}p{8cm}}
Advisor:	\theadvisors
~ & ~ \\
\theexaminers
~ & ~\\

Start of the thesis: & \textbf{\thethesisstart}\\
Submission: & \textbf{\thethesisend}\\
\end{tabular}

\end{center}

\clearpage
}
\end{singlespace}

\thispagestyle{empty}
\mbox{}\clearpage
%
% The declaration comes here
%

\ifthenelse{\boolean{phdthesis}}{}{
\thispagestyle{empty}

% Currently (2023-07-04) all courses of the faculty are asked to supply the same declaration
% source: https://informatik.rub.de/studium/pruefungsamt/abschlussarbeiten/
\begin{otherlanguage*}{ngerman}
	{\Large\noindent%
		\ifthenelse{\boolean{project}}{\textbf{Titel des Studienprojektes / title of the study project}}{\textbf{Titel meiner Abschlussarbeit / title of the final thesis}}
	\newline}

	{\large\noindent%
	\thetitle\newline}

	\vspace{1cm}

	{\Large\noindent%
	\textbf{Eigenständigkeitserklärung}}

	\vspace{5mm}

	\noindent%
	Hiermit erkläre ich, dass ich keine Arbeit in gleicher oder ähnlicher Fassung bereits als Prüfungsleistung an der Ruhr-Universität Bochum oder einer anderen Hochschule eingereicht habe.\\[2mm]
	Ich versichere, dass die vorliegende Arbeit auf meiner konzeptionellen, methodischen und inhaltlichen Eigenleistung basiert und ich keine anderen als die angegebenen Quellen und Hilfsmittel benutzt habe.
	Alle direkten und indirekten Zitate sowie KI-generierten fachlichen Inhalte habe ich unter Angabe der Quellen kenntlich gemacht.
Diese Versicherung bezieht sich auf alle Textbausteine, Tabellen, Codes, Grafiken und andere Abbildungen.
	Mir ist bewusst, dass die Unterlassung der angemessenen Dokumentation mit einem Täuschungsversuch aufgrund der Verwendung nicht zulässiger Hilfsmittel gleichzusetzen ist.\\[2mm]
	Im Falle der Verwendung von KI-Tools habe ich allen Output sorgfältig geprüft und übernehme die volle Verantwortung für eventuell durch die KI generierte fehlerhafte oder verzerrte Inhalte, fehlerhafte Referenzen, Verstöße gegen das Datenschutz- und Urheberrecht oder Plagiate.\\[2mm]
	Ich erkläre mich außerdem damit einverstanden, dass die digitale Version dieser Arbeit zwecks Plagiatsprüfung verwendet wird.
\end{otherlanguage*}

\vspace{1.5cm}

\begin{otherlanguage*}{american}
	{\Large\noindent%
	\textbf{Declaration of Authorship}}

	\vspace{5mm}

	\noindent%
	I hereby declare that I have never before submitted this paper in this or similar form for examination at Ruhr-Universität Bochum or any other institution or university.\\[2mm]
	I profess that this paper is the result of my own conceptional, methodical and analytical work and that I have not used any sources or tools other than the ones stated.
	Any quotes, whether direct or indirect, and any substantial content that was generated with the help of AI have been fully disclosed by using proper marking and quotation.
	This declaration is valid for all textual elements, charts, codes, images and figures.
	I am aware that neglecting the proper documentation constitutes an attempt at deception by use of unauthorized aid.\\[2mm]
	When using AI tools, I have critically reviewed and verified all output and assume full responsibility for any misrepresented or falsified content, faulty references, plagiarism and breaches of data protection or copyright laws that may result from the use of
generative AI.\\[2mm]
	I furthermore agree that the digital version of this thesis will be used to subject the paper to plagiarism examination.\\[2mm]
	Not this English translation but only the official version in German is legally binding.
\end{otherlanguage*}

\vspace{1.5cm}
\noindent%
\fbox{% the frame and its padding stay inside the text block
	\begin{minipage}{\dimexpr\textwidth-2\fboxsep-2\fboxrule\relax}
	Beim Verfassen dieser Arbeit habe ich die unten aufgeführten KI-Tools für folgende Zwecke verwendet:\\
	\textit{In writing this paper, I have used the AI tools specified below for the following purposes:}

	\vspace{0.5cm}
	{\noindent%
	\begin{minipage}[b]{.95\textwidth}
		\theaitools
		\vspace{0.25cm}
	\end{minipage}%
	}%

	Insofern KI-Tools für die konzeptionelle Erarbeitung der Inhalte oder der Implementierung genutzt wurden, habe ich diese in den jeweiligen Kapiteln oder im KI-Anhang vermerkt.\\
	\textit{In case AI tools were used for the conceptual design of the work of this thesis or the implementation, I have referenced the tools and their use in the respective chapters or the AI Appendix.}

	\vspace*{0.25cm}
	Ich bestätige hiermit, dass ich keine KI-Tools zur Generierung vollständiger Textabschnitte verwendet habe.\\
	\textit{I hereby confirm that I have not used AI tools for generating entire text sections.}
	\end{minipage}% no space inside the frame
}

\vspace{3cm}
\noindent
\begin{tikzpicture}
	\node (date) at (0, 0) {\normalfont Bochum, \thedate};

	\node (author) at (.5\textwidth, -1) {\normalfont(\theauthor)};
	\draw (author.north west) -- ++(.4\textwidth, 0);
\end{tikzpicture}

\cleardoublepage
}

}

%
% workaround for a bug in texlive 2016's titlesec package that prevents section
% numbers from being shown, cf.
% https://tex.stackexchange.com/questions/299969/titlesec-loss-of-section-numbering-with-the-new-update-2016-03-15
%
\RequirePackage{etoolbox}
\makeatletter
\patchcmd{\ttlh@hang}{\parindent\z@}{\parindent\z@\leavevmode}{}{}
\patchcmd{\ttlh@hang}{\noindent}{}{}{}
\makeatother

% -----------------------------------------------------------------------------

