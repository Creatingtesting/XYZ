import streamlit as st
import requests
from urllib.parse import urlparse, parse_qs, unquote
import base64
import re
import time

# Streamlit app configuration
st.set_page_config(page_title="Ultimate Link Bypass Tool", page_icon="🔗", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a2a6c, #2a5298, #1e3c72);
        color: white;
    }
    .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.2);
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
    }
    .stButton > button {
        background: linear-gradient(to right, #ff7e5f, #feb47b);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    }
    .stSelectbox > div > div > div {
        background: rgba(0, 0, 0, 0.2);
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
    }
    .result {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 1rem;
        margin-top: 1rem;
    }
    .disclaimer {
        background: rgba(255, 0, 0, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
        font-size: 0.9rem;
        text-align: center;
    }
    h1 {
        background: linear-gradient(to right, #ff7e5f, #feb47b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# Function to bypass links
def bypass_link(link, method):
    result = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Method 1: Direct parameter extraction
    if method in ['direct', 'auto']:
        try:
            parsed_url = urlparse(link)
            query_params = parse_qs(parsed_url.query)
            
            # Check for common target parameters
            param_names = ['target', 'url', 'destination', 'redirect', 'to', 'link', 'u']
            for param in param_names:
                if param in query_params:
                    result = unquote(query_params[param][0])
                    break
            
            # Manual decoding for path if no query param
            if not result:
                path_parts = parsed_url.path.split('/')
                if path_parts:
                    try:
                        decoded = base64.b64decode(path_parts[-1]).decode('utf-8')
                        if decoded.startswith('http'):
                            result = decoded
                    except:
                        pass
        except Exception as e:
            st.error(f"Direct extraction failed: {str(e)}")

    # Method 2: API Bypass using specialized services
    if (method in ['api', 'auto']) and not result:
        apis = [
            f"https://bypass.bot.nu/bypass2?url={requests.utils.quote(link)}",
            f"https://api.bypass.vip/?url={requests.utils.quote(link)}",
            f"https://bypass.pm/bypass?url={requests.utils.quote(link)}"
        ]
        for api_url in apis:
            try:
                response = requests.get(api_url, headers=headers, timeout=10)
                if response.ok:
                    data = response.json()
                    if 'destination' in data:
                        result = data['destination']
                        break
            except Exception as e:
                st.warning(f"API {api_url} failed: {str(e)}")

    # Method 3: Proxy method with content extraction
    if (method in ['proxy', 'auto']) and not result:
        proxy_urls = [
            'https://api.codetabs.com/v1/proxy?quest=',
            'https://corsproxy.io/?',
            'https://api.allorigins.win/raw?url='
        ]
        for proxy_url in proxy_urls:
            try:
                full_url = proxy_url + requests.utils.quote(link)
                response = requests.get(full_url, headers=headers, timeout=10)
                if response.ok:
                    # Check for redirection
                    if response.url != link and 'linkvertise.com' not in response.url and 'loot-link.com' not in response.url:
                        result = response.url
                        break
                    else:
                        # Extract from content
                        text = response.text
                        url_patterns = [
                            r'window\.location\.href\s*=\s*["\']([^"\']+)["\']',
                            r'window\.open\(["\']([^"\']+)["\']',
                            r'url:\s*["\']([^"\']+)["\']',
                            r'https?:\/\/[^"\']+\.(zip|rar|7z|pdf|mp4|mp3|exe|dmg|apk)',
                            r'(https?:\/\/[^\s<>"\']+)'
                        ]
                        for pattern in url_patterns:
                            match = re.search(pattern, text, re.IGNORECASE)
                            if match and match.group(1).startswith('http') and 'linkvertise.com' not in match.group(1) and 'loot-link.com' not in match.group(1):
                                result = match.group(1)
                                break
                        if result:
                            break
            except Exception as e:
                st.warning(f"Proxy {proxy_url} failed: {str(e)}")

    if not result:
        raise ValueError("Could not bypass this link. It may have advanced protections.")

    return result

# Main UI
st.title("Ultimate Link Bypass Tool")
st.markdown("Bypass LootLink, Linkvertise, and other ad-heavy links with our advanced bypass technology.")

link = st.text_input("Paste your LootLink or Linkvertise link here...", placeholder="https://example.com/...")
method = st.selectbox("Bypass Method", ["auto", "direct", "proxy", "api"], index=0)

if st.button("Bypass Link"):
    if not link:
        st.error("Please enter a link to bypass.")
    elif not link.startswith('http'):
        st.error("Please enter a valid URL starting with http:// or https://.")
    else:
        with st.spinner("Bypassing link..."):
            time.sleep(1)  # Simulate processing time
            try:
                bypassed = bypass_link(link, method)
                st.markdown('<div class="result"><h3>Bypassed Link:</h3><p>' + bypassed + '</p></div>', unsafe_allow_html=True)
                st.markdown(f'<a href="{bypassed}" target="_blank"><button>Open in New Tab</button></a>', unsafe_allow_html=True)
                # For copy, use HTML/JS snippet
                st.markdown(f"""
                    <button onclick="navigator.clipboard.writeText('{bypassed}').then(() => alert('Copied!'))">Copy Link</button>
                """, unsafe_allow_html=True)
            except ValueError as ve:
                st.error(str(ve))
            except Exception as e:
                st.error(f"Failed to bypass link: {str(e)}")

# Clear button
if st.button("Clear"):
    st.experimental_rerun()

# Instructions
with st.expander("How to use this bypass tool"):
    st.markdown("""
    1. Copy the LootLink or Linkvertise link you want to bypass  
    2. Paste it into the input field  
    3. Select a bypass method (Auto is recommended)  
    4. Click the "Bypass Link" button  
    5. Wait a few seconds while we process your link  
    6. Copy the resulting direct link or open it directly  
    """)

# Disclaimer
st.markdown('<div class="disclaimer">Note: This tool is for educational purposes only. Some links may not bypass successfully due to server-side protections.</div>', unsafe_allow_html=True)

# Example links
with st.expander("Example Links"):
    st.markdown("""
    - **Linkvertise**: https://linkvertise.com/943752/example-redirect?target=https%3A%2F%2Fexample.com  
    - **LootLink**: https://loot-link.com/s?1jQ6l9Dz  
    """)
