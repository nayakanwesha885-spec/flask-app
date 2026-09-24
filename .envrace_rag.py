import time
from app import retrieve_pages, translate_answer
question='What is patent registration in India?'
topic='General'; language='English'
t=time.time(); pages=retrieve_pages(question, topic); print('PAGES', round(time.time()-t,2), len(pages));
t=time.time(); excerpts=[]; sources=[]
for page in pages:
    excerpt = page['text'][:700].strip(); excerpts.append(f"{excerpt} [{page['filename']}, page {page['page']}]")
    source = f"{page['filename']} (Page {page['page']})"
    if source not in sources:
        sources.append(source)
answer=("Based on the retrieved local knowledge-base documents, here are the most relevant findings:\n\n" + "\n\n".join(f"- {excerpt}" for excerpt in excerpts) + "\n\nThis is educational guidance only. Verify current legal or regulatory requirements with official sources or a qualified professional.")
print('BUILD', round(time.time()-t,2), len(answer));
t=time.time(); out=translate_answer(answer, language); print('TRANSLATE', round(time.time()-t,2), len(out)); print('DONE', len(out))
