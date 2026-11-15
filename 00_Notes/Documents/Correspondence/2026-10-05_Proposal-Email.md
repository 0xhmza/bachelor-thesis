**To:** Dr. Kavous Salehzadeh Niksirat (MPI-SP)
**Subject:** Bachelor's thesis proposal — privacy harm communication in fitness and fertility tracking apps
**Attachment:** `proposal.pdf`

---

Dear Dr. Salehzadeh Niksirat,

Thank you again for our meeting on 4 September and for the reading list and
written input you sent the following day. Both shaped the proposal directly.
I have attached it as a PDF. It has four pages of content, followed by the
references and a one-page worked example of the coding. I know this is longer
than the three pages you suggested; if you would prefer a shorter version, I
will gladly condense it.

**The approach in brief**

The study is a structured content analysis of how providers of fitness and
fertility/period tracking apps communicate possible privacy harms. It covers
50 highly rated apps from the German Google Play and App Store (30 fitness,
20 fertility) and analyses their privacy policies, store listings and provider
websites, with privacy blog posts and advertisements as a supplement. A manual
cognitive walkthrough of 12 of these apps adds the communication users see
inside the app. Your research question is kept word for word and divided into
four sub-questions: which harms are mentioned (coverage), how they are
presented (stance), what protection is claimed (protection), and whether this
differs between policy, listing, website and interface (surfaces).

**Where the methodology comes from**

- **Harm model:** Following your suggestion, I based the analysis on
  Knabenhans et al.'s definition of harm and their harm trees (system
  components → capabilities such as inference → harms). Before coding, I will
  build a reference tree for each domain from the tracker literature,
  including your survey on wearable activity trackers. The trees describe
  possible harms; they are not claims about what any specific app does.
- **Harm categories:** I use the seven categories in Knabenhans et al.
  (Appendix A), which draw on Citron and Solove. Because their list omits
  Citron and Solove's relationship harms, which seem important for cycle
  tracking, I keep these as a separate tag.
- **Protection claims:** The coding of PET claims follows Martin et al.'s three
  principles and asks whether protection is framed as limiting data flows or as
  preventing harm.
- **Stance:** The categories for how a named harm is presented (acknowledged,
  qualified, minimised, shifted to the user, denied) are adapted from Zou et
  al.'s analysis of breach notifications.
- **Walkthrough:** Wharton et al.'s cognitive walkthrough, adapted so that the
  tasks are privacy tasks, such as finding out what is inferred or what happens
  after a breach.

**How I have tried to implement your points**

- *Silence on inference, breaches and incidents* (meeting, 4 Sept): these are
  coded explicitly, and two walkthrough tasks look for them in the app.
- *Sources per app, including advertisements* (4 Sept): policy, store listing,
  website and walkthrough form the core material. Advertisements and privacy
  blogs are a supplement, because ad delivery cannot be reproduced, so a
  missing ad is not treated as a finding.
- *LLM-assisted analysis with versioned prompts; manual walkthroughs* (4 Sept):
  prompts and the model are chosen in a five-app pilot and then frozen, and
  every run is logged. The model acts only as a screener: all harm mentions are
  checked by hand, and the walkthroughs are fully manual.
- *Existing LLM tools for privacy policies* (5 Sept): I looked at Polisis and
  recent LLM approaches (e.g. Rodriguez et al.). They code data practices
  rather than harms, so I propose a harm-focused coding scheme. Its output will
  be validated against my blind manual coding of ten apps, with a separate
  check for missed mentions.
- *Active literature search* (5 Sept): searches cover privacy harms, tracker
  security and privacy, and methods, and are logged. The closest work I have
  found so far is Malki et al., Zou et al., Doan et al. and Moniz and Almeida.
  As far as I can tell, none of them combines harm coverage, stance and
  protection claims across several communication surfaces, but the literature
  review is still ongoing.

**Decisions I made that I would like you to check**

- I adopted document and interface analysis as the study design, as I
  understood from your written input. The user survey described in the thesis
  offer is left as a possible later phase.
- I narrowed the scope to fitness and fertility/period apps, as listed in your
  written scope, rather than all health-tracking apps.
- "Highest rated" is defined as at least 1,000 ratings, ranked by average
  rating. I record the store category but do not rank by it.
- The German text is primary; English is used only where no German version
  exists.

**Questions**

1. Is the overall methodology suitable for a bachelor's thesis, and is its
   scope realistic for the three-month period? To be safe, I have defined a
   minimum version of the study that the pilot will check first.
2. Does my use of Knabenhans et al.'s harm trees and categories reflect how you
   intended the paper to be used, or would you weight Citron and Solove more
   strongly?
3. Would it be possible for someone at MPI-SP to act as a second coder for a
   small set of difficult decisions? If not, would you be willing to review a
   sample of them?
4. Do the data collection and walkthroughs need a formal ethics review at
   MPI-SP or at RUB, or is a written confirmation sufficient?
5. Is there a language model or computing setup at MPI-SP that you would
   recommend I use for the LLM step?

Above all, I would be very grateful for any suggestions on how to improve the
methodology, or for literature I may have missed. I am happy to discuss the
proposal in a meeting, or to move it into a shared Google Doc if you would
prefer to comment there.

Thank you very much for your time and guidance.

Kind regards,
Hamza Sghaier
B.Sc. IT-Sicherheit / Informationstechnik, Ruhr University Bochum
