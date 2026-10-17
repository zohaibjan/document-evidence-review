import io
import json
import streamlit as st
from pypdf import PdfReader
from review import build_prompt, validate_result
from snowflake_client import get_session, complete

st.set_page_config(page_title='Document Evidence Review', layout='wide')
st.title('Document Evidence Review')
st.caption('Compare a claim with uploaded evidence, inspect exact quotes, then make your own decision.')
st.info('Extracted text is sent to your configured Snowflake Cortex service. Use synthetic or authorised documents. Scanned PDFs require OCR before upload.')
claim = st.text_area('Claim to check')
files = st.file_uploader('Evidence documents', type=['pdf','txt'], accept_multiple_files=True)
if st.button('Review evidence', disabled=not files or not claim.strip()):
    session = None
    try:
        documents = []
        for index, file in enumerate(files, 1):
            if file.size > 10 * 1024 * 1024:
                raise ValueError('Maximum file size is 10 MB.')
            text = '\n'.join(page.extract_text() or '' for page in PdfReader(io.BytesIO(file.getvalue())).pages) if file.name.lower().endswith('.pdf') else file.getvalue().decode('utf-8')
            documents.append({'name': f'{index}: {file.name}', 'text': text})
        prompt = build_prompt(claim, documents)
        session = get_session()
        result = validate_result(complete(session, prompt), documents)
        st.json(result)
        st.download_button('Download review JSON', json.dumps(result, indent=2), 'evidence-review.json', 'application/json')
    except ValueError as error:
        st.error(str(error))
    except Exception:
        st.error('Review failed. Check readable input, credentials, model access and Snowflake permissions.')
    finally:
        if session is not None:
            session.close()
