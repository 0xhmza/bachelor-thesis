"""Produce one standalone .tex with all reproduction steps and embedded code."""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
RUN = BASE / 'raw/20261011T161853545650Z'
OUT = BASE / 'processed' / RUN.name

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def esc(text):
    text = str(text)
    return ''.join({'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
        '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}'}.get(c, c) for c in text)

summary = load(OUT / 'summary.json')
sessions = load(OUT / 'sessions.json')
protocol = load(RUN / 'protocol.json')
requests = load(RUN / 'requests.json')
rows = load(OUT / 'listings.json')
samsung_play = next(r for r in rows if r['platform'] == 'play')
samsung_apple = next(r for r in rows if r['listing_id'] == 'apple:1224541484')
code = (BASE / 'sampling.py').read_text(encoding='utf-8')
code_hash = hashlib.sha256((BASE / 'sampling.py').read_bytes()).hexdigest()
source_hash_rows = '\n'.join(esc(r['file']) + ' & ' + str(r['status']) +
    r' & \texttt{' + r['sha256'][:32] + r'}\newline\texttt{' + r['sha256'][32:] + r'} \\' for r in requests)
keyword_rows = '\n'.join(esc(k) + ' & ' + esc(domain) + ' & ' + esc(term) + ' & ' +
    str(next(s['count'] for s in sessions if s['keyword_id'] == k)) + r' \\' for k, domain, term in protocol['keywords'])
template = r'''\documentclass[10pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[margin=22mm]{geometry}
\usepackage{lmodern,booktabs,longtable,array,amsmath,xcolor,enumitem,listings,fancyhdr}
\usepackage[hyphens]{url}
\usepackage[colorlinks=true,linkcolor=teal,urlcolor=teal]{hyperref}
\definecolor{studyblue}{HTML}{173D50}
\definecolor{studyteal}{HTML}{176A6C}
\definecolor{linegray}{HTML}{CBD8DE}
\setlength{\parindent}{0pt}
\setlength{\parskip}{6pt}
\setlength{\emergencystretch}{3em}
\setlist{nosep,leftmargin=*}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small Germany app sampling: instance 2}
\fancyhead[R]{\small 11 October 2026}
\fancyfoot[L]{\small Execution incomplete: final ranking not available}
\fancyfoot[R]{\thepage}
\setlength{\headheight}{14pt}
\lstset{language=Python,basicstyle=\ttfamily\scriptsize,breaklines=true,
 columns=fullflexible,keepspaces=true,showstringspaces=false,
 frame=single,rulecolor=\color{linegray},aboveskip=8pt,belowskip=8pt}
\title{\color{studyblue}German App-Store Sampling by Combined Downloads\\
\large Final-sampling protocol, second collection and evidence report}
\author{Bachelor-thesis research workspace}
\date{11 October 2026}
\begin{document}
\maketitle
\begin{center}\fbox{\parbox{0.91\linewidth}{\textbf{Execution status.}
The second metadata collection was executed. The requested final download-ranked
sample could not be computed: comparable German download figures and complete
two-store discovery evidence were not available. No provisional set is certified
as final, and no missing count is filled with zero.}}
\end{center}
\tableofcontents

\section{Request, change of metric and completed work}
The requested design retains all 19 keywords from the first sampling instance,
searches German storefronts, matches identical products across Google Play and the
Apple App Store, sums comparable German download counts, and ranks products across
both stores. The user subsequently confirmed that Germany applies to the download
figures themselves, not only to the storefront. The document sample target remains
30 fitness and 20 fertility products from the proposal.

This explicitly changes the proposal's selection variable from average ratings
to combined downloads. The original proposal file was not edited. Its threshold
of at least 1,000 ratings remains a screening rule in the completion procedure;
average ratings cease to determine order. A product with a qualifying listing
retains captured counterparts for matching and download aggregation, including
counterparts with fewer ratings. Downloads must not be discarded merely because
a counterpart fails the rating threshold.

The common observation period is \textbf{1 October 2025--30 September 2026}, the
last twelve complete calendar months preceding this run. This is a declared
operational choice for the new design. No counts for this period were obtained.
One consistently defined download metric and one provider must cover both stores.
First-time downloads are preferable if the chosen provider documents that
definition consistently; do not infer it from a generic ``downloads'' label.

\begin{tabular}{L{97mm}r}\toprule
Observed outcome & Number\\\midrule
Successful German Apple keyword API searches & 19\\
Keyword-result appearances & @@APPEARANCES@@\\
Distinct Apple apps in keyword results & 179\\
Additional Samsung Health iOS lookup & 1\\
Samsung Health Play product-page capture & 1\\
Distinct captured listings in this instance & @@LISTINGS@@\\
Completed Play keyword searches & 0\\
Verified German download values & 0\\
Final ranked sample & Not available\\\bottomrule
\end{tabular}

The fresh Apple result pool is catalog evidence, not a final sampling frame.
Its API positions have not been validated as native-store search positions.
The first instance's Android seeds and 50-product working set were not reused
as if they were new keyword results. The current run ID is
\texttt{20261011T161853545650Z}; timestamps are in UTC.

\section{Why a final German-download ranking is currently unavailable}
Apple's public Search API provides metadata, not arbitrary developers' download
counts. Apple download analytics require authorised App Store Connect access
\cite{appleapi,appleanalytics}. Google's embedded install integer, often named
\texttt{realInstalls}, is not documented here as German downloads or as a
period-specific count. Setting \texttt{gl=de} cannot establish that interpretation.
These public store values therefore do not supply the requested common metric.

Appfigures documents modeled download reports with explicit product, country and
date dimensions; its estimates endpoint requires eligible plan access
\cite{estimates}. During public browser inspection, Samsung Health's unified
profile showed an estimate labelled \emph{Worldwide, September 2026}, with a rounded
display of 310K. Selecting Germany opened the message ``Create a free account to
continue''. That message proves sign-in is required at that point; it does not
prove that a free account would unlock complete historical German data. The user
confirmed having no account or export. No account was created or subscription
purchased. The worldwide value was not substituted for German data.

Consequently, an evidence-based numerical final sample cannot be produced from
the accessible data in this session. This is a source-access and measurement gap,
not a computational difficulty. The sum and ranking procedure below is executable
when its required evidence inputs are present.

\section{Fixed keyword frame}
The keyword list is identical to the first instance. Neither Samsung Health nor
another provider name was added as a keyword. The following column records the
actual count returned by each fresh Apple API request, capped by a requested
limit of 20. Fewer than 20 results were not padded with invented apps.

\begin{longtable}{L{10mm}L{22mm}L{95mm}r}
\toprule ID & Domain & Keyword & Returned\\\midrule\endhead
@@KEYWORDS@@
\bottomrule\end{longtable}

For the complete final frame, capture the first 20 organic results in default
order for every keyword in each German store: 38 sessions, at most 760 appearances.
Record advertisements separately; they do not occupy an organic slot. If the
store genuinely exhausts results sooner, preserve evidence of exhaustion.
The collection window is seven days per store. Record device, OS, account state,
storefront, exact keyword, time, listing ID and position, and archive the result
evidence. Logged-out collection is preferred where supported.

Native-store UI captures or a licensed keyword-search report can supply this
frame. Document a provider-report frame as an amendment and do not claim that
provider positions reproduce every user's personalised interface.
Appfigures' Keyword Inspector documents country and store controls
\cite{keywordinspector}; access was not available here. Google Play's current
robots file disallows the automated store-search path \cite{robots}; this run
did not scrape that path or its internal RPC endpoint. The local study ethics
instructions also prefer manual or permitted retrieval. This is why the fresh
Play keyword frame remains uncollected rather than silently replaced by web seeds.

\section{Samsung Health and discovery coverage}
Samsung Health exists in both catalog sources inspected:
\begin{itemize}
\item iOS: \texttt{1224541484}, bundle \texttt{com.samsung.health}, through the
German lookup and public German listing \cite{samsungios}.
\item Play: \texttt{com.sec.android.app.shealth}, captured with
\texttt{hl=de\&gl=de} \cite{samsungplay}.
\end{itemize}
The direct lookups establish catalog presence at capture time, not installability
on every German device. The descriptions support relevant activity/body tracking.
The iOS metadata declared German and English and free installation. Policy content,
DiGA status and product-equivalence checks still require evidence before final
inclusion. The differing iOS and Android implementations must be documented even
if treated as one product.

Samsung Health occurred in \textbf{none of the 19 Apple API keyword result sets}
in this run. Its absence from the earlier trial therefore must not be interpreted
as unavailability or ineligibility. The first Play trial used a small seed list
that did not include Samsung Health, so it could not establish keyword coverage.

The user-requested Samsung check is a separately labelled \emph{coverage audit}.
It must not be given a fictitious keyword position. To admit it into the revised
final frame when keyword searches miss it, record a supplementary-frame amendment.
For systematic coverage of other major device companions, a defensible extension
is the first 20 free Health \& Fitness chart entries in each store at the same
capture time, recorded in a separate source table; this extension was not executed.
Do not add an app simply because its eventual download count is attractive.

The Play page contained a displayed band of \texttt{1.000.000.000+} and an embedded
integer of @@SAMSUNGCOUNT@@. Neither is used as a German download figure.
The German iOS lookup returned @@SAMSUNGRATINGS@@ ratings; these are ratings, not downloads.

\section{Eligibility, matching and missing data}
Before ordering products, verify each of the following with dated evidence:
\begin{enumerate}
\item German-store availability and membership in the declared keyword or
supplementary discovery frame.
\item Relevant health or body tracking. Device companions remain eligible if
they record or display tracking data, as stated in the current proposal.
\item Free installation and German or English interface text. A translated store
description alone is not evidence of interface language.
\item A reachable, relevant privacy policy. Record a retrieval failure before
deciding whether it is genuinely unreachable; HTTP 200 alone is insufficient.
\item No DiGA listing, checked against the BfArM directory \cite{diga}.
A medical-device claim alone does not establish DiGA status.
\item No duplicate product and at least one listing with 1,000 ratings.
\item Verified counterpart coverage: all relevant German iOS/Play listings of
the same product are known, or counterpart absence is evidenced.
\end{enumerate}
Identity matching uses stable IDs, developer/provider identity, product purpose
and policy evidence. A common provider or similar name alone is insufficient.
An Android and iOS version of one verified product contributes once to the sample,
with two download observations. Different products from one provider remain
separate unless the duplicate-product rule applies. Shared policies are linked
explicitly. Allocate overlap to fertility when cycle tracking is a main function.

Missing counts remain missing. For a genuinely single-store product, sum only its
verified existing listing; do not invent a zero for an unknown counterpart. If a
known counterpart has no usable count, the combined total is unavailable. Do not
exclude such products opportunistically to make ranking possible: the completeness
gap prevents claiming the final highest-download set across the eligible frame.

\section{Combined measure and final selection}
For product $a$, let $L(a)$ contain its verified German iOS and Play listings.
Use the same source, date interval and metric definition for every term:
\[
D_a^{\mathrm{DE}} = \sum_{\ell\in L(a)}
\widehat d_{\ell,\mathrm{DE},[2025\text{-}10\text{-}01,\,2026\text{-}09\text{-}30]}.
\]
The hat denotes estimates when a third-party model is used. The total counts
downloads under that source's definition, not distinct people: one person can
download on both platforms or more than once. Never mix a Play lifetime/global
integer with German iOS downloads for a recent period.

Sort all fully eligible products by descending $D_a^{\mathrm{DE}}$, then by
canonical app ID ascending for exact ties. Preserve this overall order in
\texttt{all\_download\_rankings.csv}. Select the first 30 fitness and first
20 fertility products within that order and retain their overall ranks in
\texttt{final\_sample.csv}. If either domain genuinely has too few eligible
products, retain all and report the shortfall without lowering criteria.
No average-rating tie-break is used in the new download design.

The document sample must be frozen before the five-app coding pilot, the
12 distinct alternating-platform walkthroughs and later validation selection.
Unavailable devices, payment and identity verification affect walkthrough
eligibility separately from document eligibility.

\section{Exact reproduction steps}
This document supplies the instructions and complete code; no explanation from
the chat or the earlier report is required. The evidence bundle is still needed
to reproduce this historical capture, because live stores change over time.
The LaTeX prose cannot recreate unavailable proprietary download observations.

\begin{enumerate}
\item Install Python 3.11 or later. The acquisition and ranking code uses only
the standard library. In a new directory, save the complete Appendix A code
verbatim as \texttt{sampling.py}, UTF-8. An identical executable copy accompanies
this report. Its SHA-256 is:\\
\texttt{@@CODEHASH1@@}\\\texttt{@@CODEHASH2@@}.
\item For a new collection, run the command below. It creates a new timestamped
\texttt{raw} directory and prints \texttt{RUN=...}. HTTPS verification is enabled,
request starts are spaced by 3.5 seconds, the timeout is 30 seconds, and no
country fallback or authentication is used. A host is stopped after 403/429.
The script performs the 19 Apple queries and the labelled Samsung audit; it does
not complete the missing Play search frame or fetch private download estimates.
\end{enumerate}
\begin{lstlisting}[language={}]
python -X utf8 -u sampling.py fetch
\end{lstlisting}
\begin{enumerate}[resume]
\item To reproduce the saved instance, place its unmodified raw folder beneath
the directory containing \texttt{sampling.py}. Run:
\end{enumerate}
\begin{lstlisting}[language={}]
python -X utf8 sampling.py summarize raw/20261011T161853545650Z
\end{lstlisting}
\begin{enumerate}[resume]
\item Confirm that \texttt{summary.json} reports 19 successful queries, 322
appearances and 181 distinct listings, including the two Samsung observations.
The source sidecars and Appendix B identify original bytes by SHA-256. Comparing
fresh live results with these values is not a test of exact reproducibility;
reprocessing these saved bytes is.
\item Complete and archive all 38 search sessions, eligibility decisions,
cross-store identities, counterpart checks and exclusions. A human must inspect
evidence rather than mark every flag true to populate a sample.
\item Obtain German download evidence for every eligible product's verified
listing using one source and the common period. Prefer a licensed export/API over
manually transcribing rounded display labels. Archive the original response or
export with URL/report parameters, retrieval time and SHA-256. Export rights and
source licensing must permit preserving reproducibility evidence.
\item In \texttt{processed/20261011T161853545650Z}, create the three input files
specified below. A blank download input template is generated by the script.
The product and frame templates describe required schemas, not observed results.
\item Run the ranking command only after inputs and evidence are complete:
\end{enumerate}
\begin{lstlisting}[language={}]
python -X utf8 sampling.py rank raw/20261011T161853545650Z
\end{lstlisting}
\begin{enumerate}[resume]
\item Preserve all rankings, selected IDs, domain counts, exclusions, source
hashes and the decision file versions. Freeze a dated final sample only if the
ranker succeeds and every eligible product is represented. This run deliberately
fails at step 8 because the required data are absent.
\end{enumerate}

\subsection{Download input schema}
File \texttt{downloads.csv}; one row per listing, no duplicated observations:
\begin{lstlisting}[language={}]
listing_id,country,start,end,provider,metric,downloads,evidence_file,evidence_sha256,retrieved_utc
\end{lstlisting}
Use \texttt{DE}, \texttt{2025-10-01} and \texttt{2026-09-30} in every row.
Use \texttt{apple:<trackId>} or \texttt{play:<packageId>} IDs. Provider and metric
must be identical throughout. \texttt{downloads} is a nonnegative integer from
the source; do not convert missing values to zero or a rounded K label to an
apparently exact value. Evidence paths are relative to the run's raw directory;
append the corresponding untouched evidence files there.

\subsection{Product input schema}
File \texttt{products.json}; an array of product records. Each record includes
\texttt{app\_id}, \texttt{name}, \texttt{domain}, and \texttt{listing\_ids}.
The following checks must be affirmative with actual evidence:
\begin{lstlisting}[language={}]
tracking, free_install, DE_EN_interface, policy_reachable,
not_DiGA, not_duplicate, identity_verified,
counterpart_coverage_verified, minimum_1000_ratings,
German_store_available
\end{lstlisting}
Use an \texttt{evidence} array of objects with \texttt{file} and \texttt{sha256}.
The ranker checks the evidence files' hashes and rejects unfinished records.
For absent counterparts, preserve the dated search/catalog check that supports
absence. One listing ID cannot contribute to two products.

\subsection{Frame input schema}
File \texttt{frame\_review.json}; fields \texttt{discovery\_complete} and
\texttt{sessions}. The latter contains exactly one record for every store-keyword
pair (38). Each session has \texttt{platform} (apple/play),
\texttt{keyword\_id}, \texttt{storefront} (DE), \texttt{method}
(store\_ui\_capture/licensed\_keyword\_report), \texttt{result\_listing\_ids},
\texttt{evidence\_file}, \texttt{evidence\_sha256}, and an \texttt{exhausted}
flag for fewer than 20 organic results. Include capture dates, device/account
context and any supplementary-frame amendment in the archived evidence.
Unvalidated Apple API positions are not admitted as store-UI positions.

\section{Execution audit and outstanding inputs}
All 19 fresh Apple searches succeeded. The German Samsung lookup and Play page
also succeeded. The direct HTTP attempt to archive the Appfigures estimates
documentation returned 403, and that failure was preserved; the page was read
through the web research tool instead. Public browser inspection of the provider
profile and the sign-in gate is recorded as a transcribed observation, not an
original HTTP export. It supplies access evidence, not German download data.

The final-stage executable copy was extended after collection to validate all
38 frame records, product evidence and the retained 1,000-rating screening
rule. Its appendix hash identifies that current version. The raw acquisition
snapshot records the version used for fetching; its request mechanics and
keyword list are unchanged by the final-stage validation additions.

The unresolved inputs are comparable German download reports, complete two-store
search positions, and evidence-backed eligibility/identity decisions. No
numerical final sample is attached because none can be justified from the
observations collected. Producing a 50-row final table without those inputs
would hide the exact gaps that this audit records.

Six logic tests passed using explicitly constructed temporary fixtures: correct
cross-store summation, rejection of a missing counterpart count, rejection of
the wrong country, rejection of mixed providers, rejection of incomplete search
coverage, and rejection of unverified eligibility. All 26 response hashes were
verified. Reprocessing the historical capture reproduced the same listing JSON,
and the code embedded in this document was checked byte-for-byte against the
executable copy. These checks validate mechanics and preservation; they do not
turn the missing download observations into measured data.

\begin{thebibliography}{9}
\bibitem{appleapi} Apple, Search API documentation, accessed 11 October 2026.
\url{https://performance-partners.apple.com/search-api}.
\bibitem{appleanalytics} Apple, Analytics Reports API access and roles.
\url{https://developer.apple.com/help/app-store-connect-analytics/overview/analytics-reports-api}.
\bibitem{estimates} Appfigures, App Intelligence estimates API.
\url{https://docs.appfigures.com/api/reference/v2/estimates}.
\bibitem{keywordinspector} Appfigures, Keyword Inspector.
\url{https://help.appfigures.com/en/article/keyword-inspector-1jy20tk/}.
\bibitem{robots} Google Play, robots.txt; archived in this instance.
\url{https://play.google.com/robots.txt}.
\bibitem{samsungios} Apple, Samsung Health, German listing.
\url{https://apps.apple.com/de/app/samsung-health/id1224541484}.
\bibitem{samsungplay} Google Play, Samsung Health, German listing parameters.
\url{https://play.google.com/store/apps/details?id=com.sec.android.app.shealth&hl=de&gl=de}.
\bibitem{diga} BfArM, DiGA directory; designated source for pending checks.
\url{https://diga.bfarm.de/de/verzeichnis}.
\end{thebibliography}

\clearpage\appendix
\section{Complete executable source}
Copy the entire following listing into \texttt{sampling.py}. The keyword list,
request parameters, acquisition, parser, evidence checks, summation and ranking
are all contained here. This code does not supply missing proprietary observations.
\begin{lstlisting}
@@CODE@@
\end{lstlisting}

\clearpage\section{Raw-response integrity register}
Hashes refer to original saved bytes, including error responses. Both halves
of each SHA-256 value are one concatenated 64-character digest. Raw evidence
must be backed up separately because it is Git-ignored.
\small
\begin{longtable}{L{54mm}L{12mm}L{82mm}}
\toprule Response file & HTTP & SHA-256 (two halves)\\\midrule\endhead
@@HASHES@@
\bottomrule\end{longtable}
\end{document}
'''
replacements = {'@@APPEARANCES@@': str(summary['api_appearances']),
    '@@LISTINGS@@': str(summary['distinct_listings']), '@@KEYWORDS@@': keyword_rows,
    '@@SAMSUNGCOUNT@@': f"{samsung_play['play_embedded_global_proxy']:,}",
    '@@SAMSUNGRATINGS@@': f"{samsung_apple['rating_count']:,}",
    '@@CODEHASH1@@': code_hash[:32], '@@CODEHASH2@@': code_hash[32:],
    '@@CODE@@': code, '@@HASHES@@': source_hash_rows}
for key, value in replacements.items():
    template = template.replace(key, value)
(BASE / 'sampling_report.tex').write_text(template, encoding='utf-8')
print('Saved standalone sampling_report.tex with complete executable source.')
