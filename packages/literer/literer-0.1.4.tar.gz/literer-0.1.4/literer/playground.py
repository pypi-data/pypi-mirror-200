import literer as lit
import openai

# Begin by setting API key
openai.api_key = open("api_key").readline()
s2_api_key = open("s2_api_key").readline()

# Get n_pubs=15 papers using a specific search keyword, one can also provide further
# filters, e.g., field of study, venue, or publication type (see docstring)
papers = lit.get_papers(
    "deep learning for financial forecasting", 
    n_pubs=15, api_key=s2_api_key)

# Extract the BibTeX entries and save them to a bibliography.bib file
with open("bibiliography.bib", "w") as f:
    f.write(lit.create_bibliography(papers))

# Create literature review using TeX format (matches the bibliography defined above)
lit_review = lit.summarize_papers(papers, tex_format=False)



papers = lit.get_papers(
    "deep learning", n_pubs=100, api_key=s2_api_key, venue=TOP_JOURNALS["Economics"][:5]
)

for p in papers:
    print(p["venue"])




# Gather papers from top journals related to a specific topic
