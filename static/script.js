const translations = {
    English: {
        pageTitle: "TATVA | Ayurveda Knowledge Desk",
        clearChat: "Clear Chat",
        heroTitle: "Intellectual Property Guidance<br>for Ayurveda",
        heroDescription: "Ask questions about patents, trademarks, geographical indications, traditional knowledge and Ayurveda regulations.",
        languageLabel: "Language",
        topicLabel: "Topic",
        askLabel: "Ask TATVA",
        questionPlaceholder: "Example: What are the requirements for patenting an Ayurvedic invention in India?",
        knowledgeBaseNote: "Answers are generated using the TATVA knowledge base.",
        safetyNote: "For educational guidance only. This service does not replace a qualified legal or healthcare professional.",
        askButton: "Ask TATVA",
        searchingMessage: "Searching TATVA knowledge base...",
        responseLabel: "TATVA RESPONSE",
        answerHeading: "Answer",
        thinking: "TATVA is thinking...",
        emptyQuestion: "Please enter a question.",
        noAnswer: "No answer was returned.",
        requestError: "Something went wrong. Please try again.",
        voiceListening: "Listening...",
        voiceReady: "Voice query captured.",
        voiceError: "Microphone input was not available. Please try again.",
        voicePermission: "Please allow microphone access in your browser and try again.",
        voiceNoSpeech: "No speech was detected. Please speak clearly and try again.",
        quotaExceeded: "The OpenAI API limit has been reached. Please try again later.",
        sourcesHeading: "Sources",
        noCitation: "No document citation was returned; verify this information before acting.",
        topicGeneral: "General",
        topicPatents: "Patents",
        topicTrademarks: "Trademarks",
        topicGeographical: "Geographical Indications",
        topicCopyright: "Copyright",
        topicDesigns: "Designs",
        topicRegulations: "Ayurveda Regulations",
        topicTraditionalKnowledge: "Traditional Knowledge",
        footerText: "TATVA • RAG-based Intellectual Property & Ayurveda Assistant"
    },
    Hindi: {
        pageTitle: "TATVA | आयुर्वेद ज्ञान डेस्क",
        clearChat: "चैट साफ़ करें",
        heroTitle: "आयुर्वेद के लिए<br>बौद्धिक संपदा मार्गदर्शन",
        heroDescription: "पेटेंट, ट्रेडमार्क, भौगोलिक संकेत, पारंपरिक ज्ञान और आयुर्वेद नियमों के बारे में प्रश्न पूछें।",
        languageLabel: "भाषा",
        topicLabel: "विषय",
        askLabel: "TATVA से पूछें",
        questionPlaceholder: "उदाहरण: भारत में आयुर्वेदिक आविष्कार का पेटेंट कराने की आवश्यकताएँ क्या हैं?",
        knowledgeBaseNote: "उत्तर TATVA ज्ञान आधार का उपयोग करके तैयार किए जाते हैं।",
        safetyNote: "केवल शैक्षिक मार्गदर्शन के लिए। यह सेवा योग्य कानूनी या स्वास्थ्य पेशेवर का विकल्प नहीं है।",
        askButton: "TATVA से पूछें",
        searchingMessage: "TATVA ज्ञान आधार में खोज जारी है...",
        responseLabel: "TATVA का उत्तर",
        answerHeading: "उत्तर",
        thinking: "TATVA सोच रहा है...",
        emptyQuestion: "कृपया अपना प्रश्न लिखें।",
        noAnswer: "कोई उत्तर प्राप्त नहीं हुआ।",
        requestError: "कुछ गलत हुआ। कृपया फिर प्रयास करें।",
        quotaExceeded: "Gemini API की दैनिक सीमा पूरी हो गई है। कृपया कुछ समय बाद फिर प्रयास करें।",
            sourcesHeading: "स्रोत",
            noCitation: "कोई दस्तावेज़ स्रोत नहीं मिला; कार्रवाई से पहले जानकारी सत्यापित करें।",
        topicGeneral: "सामान्य",
        topicPatents: "पेटेंट",
        topicTrademarks: "ट्रेडमार्क",
        topicGeographical: "भौगोलिक संकेत",
        topicCopyright: "कॉपीराइट",
        topicDesigns: "डिज़ाइन",
        topicRegulations: "आयुर्वेद नियम",
        topicTraditionalKnowledge: "पारंपरिक ज्ञान",
        footerText: "TATVA • आयुर्वेद और बौद्धिक संपदा के लिए RAG आधारित सहायक"
    },
    Odia: {
        pageTitle: "TATVA | ଆୟୁର୍ବେଦ ଜ୍ଞାନ ଡେସ୍କ",
        clearChat: "ଚାଟ୍ ସଫା କରନ୍ତୁ",
        heroTitle: "ଆୟୁର୍ବେଦ ପାଇଁ<br>ବୌଦ୍ଧିକ ସମ୍ପତ୍ତି ମାର୍ଗଦର୍ଶନ",
        heroDescription: "ପେଟେଣ୍ଟ, ଟ୍ରେଡମାର୍କ, ଭୌଗୋଳିକ ସୂଚକ, ପାରମ୍ପରିକ ଜ୍ଞାନ ଏବଂ ଆୟୁର୍ବେଦ ନିୟମ ବିଷୟରେ ପ୍ରଶ୍ନ ପଚାରନ୍ତୁ।",
        languageLabel: "ଭାଷା",
        topicLabel: "ବିଷୟ",
        askLabel: "TATVA କୁ ପଚାରନ୍ତୁ",
        questionPlaceholder: "ଉଦାହରଣ: ଭାରତରେ ଆୟୁର୍ବେଦିକ ଉଦ୍ଭାବନ ପାଇଁ ପେଟେଣ୍ଟ ଆବଶ୍ୟକତା କ’ଣ?",
        knowledgeBaseNote: "ଉତ୍ତରଗୁଡ଼ିକ TATVA ଜ୍ଞାନ ଆଧାର ବ୍ୟବହାର କରି ପ୍ରସ୍ତୁତ ହୁଏ।",
        safetyNote: "କେବଳ ଶିକ୍ଷାମୂଳକ ମାର୍ଗଦର୍ଶନ ପାଇଁ। ଏହି ସେବା ଯୋଗ୍ୟ ଆଇନ କିମ୍ବା ସ୍ୱାସ୍ଥ୍ୟ ବିଶେଷଜ୍ଞଙ୍କ ବିକଳ୍ପ ନୁହେଁ।",
        askButton: "TATVA କୁ ପଚାରନ୍ତୁ",
        searchingMessage: "TATVA ଜ୍ଞାନ ଆଧାରରେ ଖୋଜା ଚାଲିଛି...",
        responseLabel: "TATVA ଉତ୍ତର",
        answerHeading: "ଉତ୍ତର",
        thinking: "TATVA ଚିନ୍ତା କରୁଛି...",
        emptyQuestion: "ଦୟାକରି ଆପଣଙ୍କ ପ୍ରଶ୍ନ ଲେଖନ୍ତୁ।",
        noAnswer: "କୌଣସି ଉତ୍ତର ମିଳିଲା ନାହିଁ।",
        requestError: "କିଛି ଭୁଲ ହୋଇଛି। ଦୟାକରି ପୁଣି ଚେଷ୍ଟା କରନ୍ତୁ।",
        quotaExceeded: "Gemini API ର ଦୈନିକ ସୀମା ପୂରଣ ହୋଇଛି। କିଛି ସମୟ ପରେ ପୁଣି ଚେଷ୍ଟା କରନ୍ତୁ।",
            sourcesHeading: "ଉତ୍ସ",
            noCitation: "କୌଣସି ଦଲିଲ ଉତ୍ସ ମିଳିଲା ନାହିଁ; କାର୍ଯ୍ୟ ପୂର୍ବରୁ ସୂଚନା ଯାଞ୍ଚ କରନ୍ତୁ।",
        topicGeneral: "ସାଧାରଣ",
        topicPatents: "ପେଟେଣ୍ଟ",
        topicTrademarks: "ଟ୍ରେଡମାର୍କ",
        topicGeographical: "ଭୌଗୋଳିକ ସୂଚକ",
        topicCopyright: "କପିରାଇଟ୍",
        topicDesigns: "ଡିଜାଇନ୍",
        topicRegulations: "ଆୟୁର୍ବେଦ ନିୟମ",
        topicTraditionalKnowledge: "ପାରମ୍ପରିକ ଜ୍ଞାନ",
        footerText: "TATVA • ଆୟୁର୍ବେଦ ଏବଂ ବୌଦ୍ଧିକ ସମ୍ପତ୍ତି ପାଇଁ RAG ଆଧାରିତ ସହାୟক"
    },
    Bengali: {
        pageTitle: "TATVA | আয়ুর্বেদ জ্ঞান ডেস্ক",
        clearChat: "চ্যাট পরিষ্কার করুন",
        heroTitle: "আয়ুর্বেদের জন্য<br>বুদ্ধিবৃত্তিক সম্পত্তির নির্দেশনা",
        heroDescription: "পেটেন্ট, ট্রেডমার্ক, ভৌগোলিক নির্দেশক, ঐতিহ্যবাহী জ্ঞান এবং আয়ুর্বেদ নিয়ম সম্পর্কে প্রশ্ন করুন।",
        languageLabel: "ভাষা",
        questionPlaceholder: "উদাহরণ: ভারতে আয়ুর্বেদিক আবিষ্কারের পেটেন্টের প্রয়োজনীয়তা কী?",
        knowledgeBaseNote: "উত্তরগুলি TATVA জ্ঞানভাণ্ডার ব্যবহার করে তৈরি করা হয়।",
        askButton: "TATVA-কে জিজ্ঞাসা করুন",
        searchingMessage: "TATVA জ্ঞানভাণ্ডারে খোঁজা হচ্ছে...",
        thinking: "TATVA ভাবছে...",
        emptyQuestion: "অনুগ্রহ করে আপনার প্রশ্ন লিখুন।",
        noAnswer: "কোনও উত্তর পাওয়া যায়নি।",
        requestError: "কিছু ভুল হয়েছে। আবার চেষ্টা করুন।",
        quotaExceeded: "Gemini API-এর দৈনিক সীমা শেষ হয়ে গেছে। কিছুক্ষণ পরে আবার চেষ্টা করুন।",
            sourcesHeading: "উৎস",
            noCitation: "কোনও নথির উৎস পাওয়া যায়নি; কাজ করার আগে তথ্য যাচাই করুন।",
        topicGeneral: "সাধারণ",
        topicPatents: "পেটেন্ট",
        topicTrademarks: "ট্রেডমার্ক",
        topicGeographical: "ভৌগোলিক নির্দেশক",
        topicRegulations: "আয়ুর্বেদ নিয়ম",
        topicTraditionalKnowledge: "ঐতিহ্যবাহী জ্ঞান",
        pageTitle: "TATVA | আয়ুর্বেদ জ্ঞান ডেস্ক"
    }
};

const interfaceTranslations = {
    English: {
        nav: ["Home", "Ask a question", "Formulation classification", "ABS guidance", "Disclaimer", "Contact"], heroNotes: ["Ask with context", "Get a clearer starting point", "Act with confidence", "Grounded in your knowledge base"], seal: ["TRADITION", "+ INNOVATION"], loading: "Searching the knowledge base...",
        start: "Start asking ↗", heroEyebrow: "Evidence-led Ayurveda intelligence", heroTitle: "Make informed moves<br><em>with traditional knowledge.</em>", heroIntro: "A practical knowledge desk for navigating Ayurveda intellectual property, formulation pathways and access & benefit sharing with greater clarity.", ask: "Ask TATVA →", explore: "Explore the guide ↓", proof: ["Source-cited answers", "Built for India"],
        signals: [["Ask a question", "Turn uncertainty into a useful next step"], ["Classify your formulation", "Understand the regulatory conversation"], ["Navigate ABS", "Respect knowledge, share benefits"]],
        askEyebrow: "The knowledge desk", askTitle: "Bring your question.<br><em>Leave with direction.</em>", askText: "Ask about patents, trademarks, traditional knowledge, GI, copyright or Ayurveda regulations. TATVA searches the connected knowledge base and returns a source-aware response.", lens: "Choose a lens", topics: ["General", "Patents", "Trademarks", "GI", "Traditional knowledge", "Regulations"], response: "TATVA / RESPONSE", answer: "Answer", clear: "Clear chat",
        classificationEyebrow: "Formulation classification", classificationTitle: "Every formulation<br><em>has a pathway.</em>", classificationText: "Classification is the first useful conversation. Use these signals to prepare your questions, then verify the applicable route with the relevant authority or professional.", cards: [["Classical formulation", "Referenced in authoritative Ayurvedic texts and prepared according to established principles.", "Ask about this ↗"], ["Proprietary formulation", "A product developed from traditional ingredients or principles with a distinct composition or process.", "Explore IP questions ↗"], ["Novel innovation", "A new process, use or composition where novelty, evidence and documentation become central.", "Explore patent questions ↗"]],
        absEyebrow: "Access & benefit sharing", absTitle: "Respect the source.<br><em>Share the value.</em>", absText: "ABS guidance helps connect access to biological resources and associated traditional knowledge with fair, equitable benefit sharing. Think of it as a responsibility built into the innovation journey.", absPoints: ["Identify the knowledge and resource.", "Understand consent and authority.", "Document benefits and obligations."], absLink: "Ask about ABS →",
        disclaimerEyebrow: "Important context", disclaimerTitle: "Guidance is a starting point,<br><em>not a substitute for advice.</em>", disclaimerText: "TATVA is an educational information service. It does not provide legal, medical or regulatory advice, and it cannot replace current official sources or a qualified professional. Always verify time-sensitive requirements before acting.",
        contactEyebrow: "Keep the conversation going", contactTitle: "Have a question<br><em>for the desk?</em>", contactText: "For knowledge-base feedback, partnership enquiries or product questions, reach out to the team behind TATVA.", contactButton: "Contact the team ↗", contactCard: "Built for researchers, founders, practitioners and curious minds working at the intersection of Ayurveda and innovation.", contactNote: "Knowledge with context. Progress with care.", footer: "Source-cited guidance for a living tradition.", top: "Back to top ↑"
    },
    Hindi: {
        nav: ["होम", "प्रश्न पूछें", "फॉर्मूलेशन वर्गीकरण", "ABS मार्गदर्शन", "अस्वीकरण", "संपर्क"], heroNotes: ["संदर्भ के साथ पूछें", "अधिक स्पष्ट शुरुआत पाएं", "विश्वास के साथ आगे बढ़ें", "आपके ज्ञान आधार पर आधारित"], seal: ["परंपरा", "+ नवाचार"], loading: "ज्ञान आधार में खोज जारी है...", start: "प्रश्न पूछें ↗", heroEyebrow: "प्रमाण-आधारित आयुर्वेद जानकारी", heroTitle: "पारंपरिक ज्ञान के साथ<br><em>समझदारी से आगे बढ़ें।</em>", heroIntro: "आयुर्वेद बौद्धिक संपदा, फॉर्मूलेशन मार्ग और लाभ-साझाकरण को समझने के लिए व्यावहारिक ज्ञान डेस्क।", ask: "TATVA से पूछें →", explore: "गाइड देखें ↓", proof: ["स्रोत-सहित उत्तर", "भारत के लिए निर्मित"], signals: [["प्रश्न पूछें", "अनिश्चितता को अगले कदम में बदलें"], ["फॉर्मूलेशन वर्गीकृत करें", "नियामक बातचीत को समझें"], ["ABS मार्गदर्शन", "ज्ञान का सम्मान, लाभ साझा करें"]], askEyebrow: "ज्ञान डेस्क", askTitle: "अपना प्रश्न लाएं।<br><em>दिशा के साथ लौटें।</em>", askText: "पेटेंट, ट्रेडमार्क, पारंपरिक ज्ञान, GI, कॉपीराइट या आयुर्वेद नियमों के बारे में पूछें।", lens: "विषय चुनें", topics: ["सामान्य", "पेटेंट", "ट्रेडमार्क", "GI", "पारंपरिक ज्ञान", "नियम"], response: "TATVA / उत्तर", answer: "उत्तर", clear: "चैट साफ़ करें", classificationEyebrow: "फॉर्मूलेशन वर्गीकरण", classificationTitle: "हर फॉर्मूलेशन का<br><em>एक मार्ग होता है।</em>", classificationText: "वर्गीकरण पहली उपयोगी बातचीत है। प्रश्न तैयार करें और संबंधित प्राधिकरण या विशेषज्ञ से मार्ग की पुष्टि करें।", cards: [["शास्त्रीय फॉर्मूलेशन", "प्रामाणिक आयुर्वेद ग्रंथों में संदर्भित और स्थापित सिद्धांतों के अनुसार तैयार।", "इसके बारे में पूछें ↗"], ["स्वामित्व फॉर्मूलेशन", "पारंपरिक सामग्री या सिद्धांतों से विकसित विशिष्ट संरचना या प्रक्रिया वाला उत्पाद।", "IP प्रश्न देखें ↗"], ["नवीन नवाचार", "नई प्रक्रिया, उपयोग या संरचना जहां नवीनता और दस्तावेज़ महत्वपूर्ण हैं।", "पेटेंट प्रश्न देखें ↗"]], absEyebrow: "पहुंच और लाभ-साझाकरण", absTitle: "स्रोत का सम्मान करें।<br><em>मूल्य साझा करें।</em>", absText: "ABS जैविक संसाधनों और पारंपरिक ज्ञान तक पहुंच को उचित और समान लाभ-साझाकरण से जोड़ता है।", absPoints: ["ज्ञान और संसाधन की पहचान करें।", "सहमति और प्राधिकरण समझें।", "लाभ और दायित्व दर्ज करें।"], absLink: "ABS के बारे में पूछें →", disclaimerEyebrow: "महत्वपूर्ण संदर्भ", disclaimerTitle: "मार्गदर्शन शुरुआत है,<br><em>सलाह का विकल्प नहीं।</em>", disclaimerText: "TATVA शैक्षिक जानकारी सेवा है। यह कानूनी, चिकित्सीय या नियामक सलाह नहीं है। कार्रवाई से पहले आधिकारिक स्रोत या योग्य विशेषज्ञ से पुष्टि करें।", contactEyebrow: "बातचीत जारी रखें", contactTitle: "डेस्क के लिए<br><em>कोई प्रश्न है?</em>", contactText: "ज्ञान-आधार प्रतिक्रिया, साझेदारी या उत्पाद प्रश्नों के लिए TATVA टीम से संपर्क करें।", contactButton: "टीम से संपर्क करें ↗", contactCard: "आयुर्वेद और नवाचार के बीच काम करने वाले शोधकर्ताओं, संस्थापकों और जिज्ञासु लोगों के लिए।", contactNote: "संदर्भ के साथ ज्ञान। सावधानी के साथ प्रगति।", footer: "जीवंत परंपरा के लिए स्रोत-सहित मार्गदर्शन।", top: "ऊपर जाएं ↑"
    }
};

interfaceTranslations.Odia = Object.assign({}, interfaceTranslations.English, {
    nav: ["ମୁଖ୍ୟ ପୃଷ୍ଠା", "ପ୍ରଶ୍ନ ପଚାରନ୍ତୁ", "ଫର୍ମୁଲେସନ ବର୍ଗୀକରଣ", "ABS ମାର୍ଗଦର୍ଶନ", "ଅସ୍ୱୀକାର", "ଯୋଗାଯୋଗ"], start: "ପ୍ରଶ୍ନ ପଚାରନ୍ତୁ ↗", heroEyebrow: "ପ୍ରମାଣ-ଆଧାରିତ ଆୟୁର୍ବେଦ ଜ୍ଞାନ", heroTitle: "ପାରମ୍ପରିକ ଜ୍ଞାନ ସହିତ<br><em>ସଚେତନ ପଦକ୍ଷେପ ନିଅନ୍ତୁ।</em>", heroIntro: "ଆୟୁର୍ବେଦ ବୌଦ୍ଧିକ ସମ୍ପତ୍ତି, ଫର୍ମୁଲେସନ ମାର୍ଗ ଏବଂ ଲାଭ ବଣ୍ଟନ ବୁଝିବା ପାଇଁ ଏକ ବ୍ୟବହାରିକ ଜ୍ଞାନ ଡେସ୍କ।", ask: "TATVA କୁ ପଚାରନ୍ତୁ →", explore: "ମାର୍ଗଦର୍ଶିକା ଦେଖନ୍ତୁ ↓", proof: ["ଉତ୍ସ ସହିତ ଉତ୍ତର", "ଭାରତ ପାଇଁ ନିର୍ମିତ"], signals: [["ପ୍ରଶ୍ନ ପଚାରନ୍ତୁ", "ଅନିଶ୍ଚିତତାକୁ ପରବର୍ତ୍ତୀ ପଦକ୍ଷେପରେ ବଦଳାନ୍ତୁ"], ["ଫର୍ମୁଲେସନ ବର୍ଗୀକରଣ", "ନିୟମର ଆଲୋଚନା ବୁଝନ୍ତୁ"], ["ABS ମାର୍ଗଦର୍ଶନ", "ଜ୍ଞାନକୁ ସମ୍ମାନ, ଲାଭ ବଣ୍ଟନ"]], askEyebrow: "ଜ୍ଞାନ ଡେସ୍କ", askTitle: "ଆପଣଙ୍କ ପ୍ରଶ୍ନ ଆଣନ୍ତୁ।<br><em>ଦିଗନିର୍ଦ୍ଦେଶ ସହିତ ଫେରନ୍ତୁ।</em>", askText: "ପେଟେଣ୍ଟ, ଟ୍ରେଡମାର୍କ, ପାରମ୍ପରିକ ଜ୍ଞାନ, GI, କପିରାଇଟ୍ କିମ୍ବା ଆୟୁର୍ବେଦ ନିୟମ ବିଷୟରେ ପଚାରନ୍ତୁ।", lens: "ବିଷୟ ବାଛନ୍ତୁ", topics: ["ସାଧାରଣ", "ପେଟେଣ୍ଟ", "ଟ୍ରେଡମାର୍କ", "GI", "ପାରମ୍ପରିକ ଜ୍ଞାନ", "ନିୟମ"], response: "TATVA / ଉତ୍ତର", answer: "ଉତ୍ତର", clear: "ଚାଟ୍ ସଫା କରନ୍ତୁ", loading: "ଜ୍ଞାନ ଆଧାରରେ ଖୋଜା ଚାଲିଛି...", classificationEyebrow: "ଫର୍ମୁଲେସନ ବର୍ଗୀକରଣ", classificationTitle: "ପ୍ରତ୍ୟେକ ଫର୍ମୁଲେସନର<br><em>ଏକ ମାର୍ଗ ଅଛି।</em>", classificationText: "ବର୍ଗୀକରଣ ହେଉଛି ପ୍ରଥମ ଉପଯୋଗୀ ଆଲୋଚନା। ପ୍ରଶ୍ନ ପ୍ରସ୍ତୁତ କରନ୍ତୁ ଏବଂ ସମ୍ପୃକ୍ତ କର୍ତ୍ତୃପକ୍ଷଙ୍କଠାରୁ ନିଶ୍ଚିତ କରନ୍ତୁ।", absEyebrow: "ପ୍ରବେଶ ଏବଂ ଲାଭ ବଣ୍ଟନ", absTitle: "ଉତ୍ସକୁ ସମ୍ମାନ କରନ୍ତୁ।<br><em>ମୂଲ୍ୟ ବଣ୍ଟନ କରନ୍ତୁ।</em>", absText: "ABS ଜୈବିକ ସମ୍ପଦ ଏବଂ ପାରମ୍ପରିକ ଜ୍ଞାନ ପ୍ରାପ୍ତିକୁ ନ୍ୟାୟସଙ୍ଗତ ଲାଭ ବଣ୍ଟନ ସହିତ ଯୋଡ଼େ।", absPoints: ["ଜ୍ଞାନ ଏବଂ ସମ୍ପଦ ଚିହ୍ନଟ କରନ୍ତୁ।", "ସମ୍ମତି ଏବଂ ଅଧିକାର ବୁଝନ୍ତୁ।", "ଲାଭ ଏବଂ ଦାୟିତ୍ୱ ଲିପିବଦ୍ଧ କରନ୍ତୁ।"], absLink: "ABS ବିଷୟରେ ପଚାରନ୍ତୁ →", disclaimerEyebrow: "ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ସୂଚନା", disclaimerTitle: "ମାର୍ଗଦର୍ଶନ ଏକ ଆରମ୍ଭ,<br><em>ପରାମର୍ଶର ବିକଳ୍ପ ନୁହେଁ।</em>", disclaimerText: "TATVA ଏକ ଶିକ୍ଷାମୂଳକ ସୂଚନା ସେବା। ଏହା ଆଇନଗତ, ଚିକିତ୍ସା କିମ୍ବା ନିୟାମକ ପରାମର୍ଶ ନୁହେଁ।", contactEyebrow: "ଆଲୋଚନା ଜାରି ରଖନ୍ତୁ", contactTitle: "ଡେସ୍କ ପାଇଁ<br><em>କିଛି ପ୍ରଶ୍ନ ଅଛି?</em>", contactText: "ଜ୍ଞାନ ଆଧାର ମତାମତ, ସହଭାଗିତା କିମ୍ବା ଉତ୍ପାଦ ପ୍ରଶ୍ନ ପାଇଁ TATVA ଦଳ ସହିତ ଯୋଗାଯୋଗ କରନ୍ତୁ।", contactButton: "ଦଳ ସହିତ ଯୋଗାଯୋଗ ↗", footer: "ଜୀବନ୍ତ ପରମ୍ପରା ପାଇଁ ଉତ୍ସ ସହିତ ମାର୍ଗଦର୍ଶନ।", top: "ଉପରକୁ ଯାଆନ୍ତୁ ↑"
});
interfaceTranslations.Bengali = Object.assign({}, interfaceTranslations.English, {
    nav: ["হোম", "প্রশ্ন করুন", "ফর্মুলেশন শ্রেণিবিন্যাস", "ABS নির্দেশনা", "দাবিত্যাগ", "যোগাযোগ"], start: "প্রশ্ন করুন ↗", heroEyebrow: "প্রমাণভিত্তিক আয়ুর্বেদ জ্ঞান", heroTitle: "ঐতিহ্যবাহী জ্ঞানের সঙ্গে<br><em>সচেতন পদক্ষেপ নিন।</em>", heroIntro: "আয়ুর্বেদ বৌদ্ধিক সম্পত্তি, ফর্মুলেশন পথ এবং সুবিধা ভাগাভাগি বোঝার জন্য একটি ব্যবহারিক জ্ঞান ডেস্ক।", ask: "TATVA-কে জিজ্ঞাসা করুন →", explore: "নির্দেশিকা দেখুন ↓", proof: ["উৎস-সহ উত্তর", "ভারতের জন্য তৈরি"], signals: [["প্রশ্ন করুন", "অনিশ্চয়তাকে পরবর্তী পদক্ষেপে বদলান"], ["ফর্মুলেশন শ্রেণিবিন্যাস", "নিয়ন্ত্রক আলোচনা বুঝুন"], ["ABS নির্দেশনা", "জ্ঞানকে সম্মান, সুবিধা ভাগ করুন"]], askEyebrow: "জ্ঞান ডেস্ক", askTitle: "আপনার প্রশ্ন আনুন।<br><em>দিকনির্দেশনা নিয়ে ফিরুন।</em>", askText: "পেটেন্ট, ট্রেডমার্ক, ঐতিহ্যবাহী জ্ঞান, GI, কপিরাইট বা আয়ুর্বেদ নিয়ম সম্পর্কে জিজ্ঞাসা করুন।", lens: "বিষয় বাছুন", topics: ["সাধারণ", "পেটেন্ট", "ট্রেডমার্ক", "GI", "ঐতিহ্যবাহী জ্ঞান", "নিয়ম"], response: "TATVA / উত্তর", answer: "উত্তর", clear: "চ্যাট পরিষ্কার করুন", loading: "জ্ঞানভাণ্ডারে খোঁজা হচ্ছে...", classificationEyebrow: "ফর্মুলেশন শ্রেণিবিন্যাস", classificationTitle: "প্রতিটি ফর্মুলেশনের<br><em>একটি পথ আছে।</em>", classificationText: "শ্রেণিবিন্যাস হল প্রথম গুরুত্বপূর্ণ আলোচনা। প্রশ্ন প্রস্তুত করুন এবং সংশ্লিষ্ট কর্তৃপক্ষের সঙ্গে পথটি যাচাই করুন।", absEyebrow: "প্রবেশাধিকার ও সুবিধা ভাগাভাগি", absTitle: "উৎসকে সম্মান করুন।<br><em>মূল্য ভাগ করুন।</em>", absText: "ABS জৈব সম্পদ ও ঐতিহ্যবাহী জ্ঞানে প্রবেশাধিকারকে ন্যায্য সুবিধা ভাগাভাগির সঙ্গে যুক্ত করে।", absPoints: ["জ্ঞান ও সম্পদ শনাক্ত করুন।", "সম্মতি ও কর্তৃত্ব বুঝুন।", "সুবিধা ও দায়বদ্ধতা নথিভুক্ত করুন।"], absLink: "ABS সম্পর্কে জিজ্ঞাসা করুন →", disclaimerEyebrow: "গুরুত্বপূর্ণ প্রসঙ্গ", disclaimerTitle: "নির্দেশনা একটি শুরু,<br><em>পরামর্শের বিকল্প নয়।</em>", disclaimerText: "TATVA একটি শিক্ষামূলক তথ্যসেবা। এটি আইনি, চিকিৎসা বা নিয়ন্ত্রক পরামর্শ প্রদান করে না।", contactEyebrow: "আলোচনা চালিয়ে যান", contactTitle: "ডেস্কের জন্য<br><em>কোনও প্রশ্ন আছে?</em>", contactText: "জ্ঞানভাণ্ডার, অংশীদারিত্ব বা পণ্য সংক্রান্ত প্রশ্নের জন্য TATVA দলের সঙ্গে যোগাযোগ করুন।", contactButton: "দলের সঙ্গে যোগাযোগ করুন ↗", footer: "জীবন্ত ঐতিহ্যের জন্য উৎস-সহ নির্দেশনা।", top: "উপরে যান ↑"
});

const additionalLanguageProfiles = {
    Assamese: ["অসমীয়া", "ঘৰ", "প্ৰশ্ন সোধক", "ফৰ্মুলেচন শ্ৰেণীবিভাজন", "ABS নিৰ্দেশনা", "দাবীত্যাগ", "যোগাযোগ", "প্ৰশ্ন সোধক ↗", "প্ৰমাণভিত্তিক আয়ুৰ্বেদ জ্ঞান"],
    Bodo: ["बड़ो", "हाबा", "सोंनाय सों", "फर्मुलेसन बर्गीकरण", "ABS बिथोन", "दाबि जाय", "फोनजाब", "सोंनाय सों ↗", "प्रमाण आधारित आयुर्वेद सोलों"],
    Dogri: ["डोगरी", "घर", "सवाल पुछो", "फार्मुलेशन वर्गीकरण", "ABS मार्गदर्शन", "अस्वीकरण", "संपर्क", "सवाल पुछो ↗", "प्रमाण-आधारित आयुर्वेद ज्ञान"],
    Gujarati: ["ગુજરાતી", "હોમ", "પ્રશ્ન પૂછો", "ફોર્મ્યુલેશન વર્ગીકરણ", "ABS માર્ગદર્શન", "અસ્વીકરણ", "સંપર્ક", "પ્રશ્ન પૂછો ↗", "પુરાવા આધારિત આયુર્વેદ જ્ઞાન"],
    Kannada: ["ಕನ್ನಡ", "ಮುಖಪುಟ", "ಪ್ರಶ್ನೆ ಕೇಳಿ", "ಸೂತ್ರೀಕರಣ ವರ್ಗೀಕರಣ", "ABS ಮಾರ್ಗದರ್ಶನ", "ಹಕ್ಕುತ್ಯಾಗ", "ಸಂಪರ್ಕ", "ಪ್ರಶ್ನೆ ಕೇಳಿ ↗", "ಪುರಾವೆ ಆಧಾರಿತ ಆಯುರ್ವೇದ ಜ್ಞಾನ"],
    Kashmiri: ["कॉशुर", "گھر", "سوال پوچھو", "فارمولیشن درجہ بندی", "ABS رنمائی", "دستبرداری", "رابطہ", "سوال پوچھو ↗", "ثبوت پر مبنی آیوروید علم"],
    Konkani: ["कोंकणी", "मुखेल पान", "प्रश्न विचारात", "फॉर्म्युलेशन वर्गीकरण", "ABS मार्गदर्शन", "अस्वीकरण", "संपर्क", "प्रश्न विचारात ↗", "पुरावो-आधारीत आयुर्वेद ज्ञान"],
    Maithili: ["मैथिली", "घर", "प्रश्न पूछू", "फॉर्मुलेशन वर्गीकरण", "ABS मार्गदर्शन", "अस्वीकरण", "सम्पर्क", "प्रश्न पूछू ↗", "प्रमाण-आधारित आयुर्वेद ज्ञान"],
    Malayalam: ["മലയാളം", "ഹോം", "ചോദ്യം ചോദിക്കുക", "ഫോർമുലേഷൻ വർഗ്ഗീകരണം", "ABS മാർഗ്ഗനിർദ്ദേശം", "നിരാകരണം", "ബന്ധപ്പെടുക", "ചോദ്യം ചോദിക്കുക ↗", "തെളിവ് അടിസ്ഥാനമാക്കിയ ആയുർവേദ അറിവ്"],
    Manipuri: ["মৈতৈলোন্", "ইমুং", "ৱাহং পাউ", "ফর্মুলেশন শ্রেণীবিভাগ", "ABS ৱারোল", "দাবিত্যাগ", "শম্নম", "ৱাহং পাউ ↗", "প্রমাণ-ভিত্তিক আয়ুর্বেদ জ্ঞান"],
    Marathi: ["मराठी", "मुख्यपृष्ठ", "प्रश्न विचारा", "फॉर्म्युलेशन वर्गीकरण", "ABS मार्गदर्शन", "अस्वीकरण", "संपर्क", "प्रश्न विचारा ↗", "पुराव्यावर आधारित आयुर्वेद ज्ञान"],
    Nepali: ["नेपाली", "गृहपृष्ठ", "प्रश्न सोध्नुहोस्", "फर्मुलेसन वर्गीकरण", "ABS मार्गदर्शन", "अस्वीकरण", "सम्पर्क", "प्रश्न सोध्नुहोस् ↗", "प्रमाणमा आधारित आयुर्वेद ज्ञान"],
    Punjabi: ["ਪੰਜਾਬੀ", "ਮੁੱਖ ਪੰਨਾ", "ਸਵਾਲ ਪੁੱਛੋ", "ਫਾਰਮੂਲੇਸ਼ਨ ਵਰਗੀਕਰਨ", "ABS ਮਾਰਗਦਰਸ਼ਨ", "ਬੇਦਾਅਵਾ", "ਸੰਪਰਕ", "ਸਵਾਲ ਪੁੱਛੋ ↗", "ਸਬੂਤ-ਆਧਾਰਿਤ ਆਯੁਰਵੇਦ ਗਿਆਨ"],
    Sanskrit: ["संस्कृतम्", "मुखपृष्ठम्", "प्रश्नं पृच्छतु", "योगवर्गीकरणम्", "ABS मार्गदर्शनम्", "अस्वीकरणम्", "सम्पर्कः", "प्रश्नं पृच्छतु ↗", "प्रमाणाधारितम् आयुर्वेदज्ञानम्"],
    Santali: ["ᱥᱟᱱᱛᱟᱲᱤ", "ᱚᱲᱟᱜ", "ᱡᱚᱛᱚᱜ ᱥᱚᱫᱚᱨ", "ᱯᱷᱚᱨᱢᱩᱞᱮᱥᱚᱱ ᱵᱟᱹᱛᱤ", "ABS ᱥᱚᱞᱦᱟ", "ᱵᱟᱹᱫ", "ᱡᱚᱯᱚᱲ", "ᱡᱚᱛᱚᱜ ᱥᱚᱫᱚᱨ ↗", "ᱯᱨᱚᱢᱟᱱ ᱟᱫᱷᱟᱨᱤᱛ ᱟᱭᱩᱨᱵᱮᱫ ᱧᱟᱱ"],
    Sindhi: ["सिन्धी", "گھر", "سوال پڇو", "فارميوليشن درجابندي", "ABS رهنمائي", "دستبرداري", "رابطو", "سوال پڇو ↗", "ثبوت تي ٻڌل ايوورويد ڄاڻ"],
    Tamil: ["தமிழ்", "முகப்பு", "கேள்வி கேளுங்கள்", "சூத்திர வகைப்பாடு", "ABS வழிகாட்டுதல்", "மறுப்பு", "தொடர்பு", "கேள்வி கேளுங்கள் ↗", "ஆதார அடிப்படையிலான ஆயுர்வேத அறிவு"],
    Telugu: ["తెలుగు", "హోమ్", "ప్రశ్న అడగండి", "ఫార్ములేషన్ వర్గీకరణ", "ABS మార్గదర్శకం", "నిరాకరణ", "సంప్రదించండి", "ప్రశ్న అడగండి ↗", "ఆధారిత ఆయుర్వేద జ్ఞానం"],
    Urdu: ["اُردُو", "گھر", "سوال پوچھیں", "تشکیل کی درجہ بندی", "ABS رہنمائی", "دستبرداری", "رابطہ", "سوال پوچھیں ↗", "ثبوت پر مبنی آیوروید علم"]
};

Object.keys(additionalLanguageProfiles).forEach(function (language) {
    const profile = additionalLanguageProfiles[language];
    const languageName = profile[0];
    const label = profile[1];
    const askLabel = profile[2];
    const classificationLabel = profile[3];
    const absLabel = profile[4];
    const disclaimerLabel = profile[5];
    const contactLabel = profile[6];
    const startLabel = profile[7];
    const identity = profile[8];
    interfaceTranslations[language] = Object.assign({}, interfaceTranslations.English, {
        nav: profile.slice(1, 7),
        start: startLabel,
        heroEyebrow: identity,
        heroTitle: identity + "<br><em>" + languageName + "</em>",
        heroIntro: identity,
        ask: startLabel,
        explore: classificationLabel,
        proof: [identity, languageName],
        signals: [[askLabel, identity], [classificationLabel, identity], [absLabel, identity]],
        askEyebrow: label,
        askTitle: askLabel + "<br><em>" + identity + "</em>",
        askText: identity,
        lens: askLabel,
        topics: [label, askLabel, classificationLabel, "GI", absLabel, disclaimerLabel],
        response: languageName + " / " + askLabel,
        answer: askLabel,
        clear: disclaimerLabel,
        classificationEyebrow: classificationLabel,
        classificationTitle: classificationLabel + "<br><em>" + identity + "</em>",
        classificationText: identity,
        cards: [[classificationLabel, identity, askLabel + " ↗"], [classificationLabel, identity, startLabel + " ↗"], [classificationLabel, identity, startLabel + " ↗"]],
        absEyebrow: absLabel,
        absTitle: absLabel + "<br><em>" + identity + "</em>",
        absText: identity,
        absPoints: [identity, identity, identity],
        absLink: absLabel + " →",
        disclaimerEyebrow: disclaimerLabel,
        disclaimerTitle: disclaimerLabel + "<br><em>" + identity + "</em>",
        disclaimerText: identity,
        contactEyebrow: contactLabel,
        contactTitle: contactLabel + "<br><em>" + identity + "</em>",
        contactText: identity,
        contactButton: contactLabel + " ↗",
        contactCard: identity,
        contactNote: identity,
        footer: identity,
        top: label + " ↑",
        heroNotes: [askLabel, identity, contactLabel, identity],
        seal: [languageName, "+ " + identity],
        loading: identity
    });
    translations[language] = {
        pageTitle: "TATVA | " + languageName,
        clearChat: disclaimerLabel,
        languageLabel: languageName,
        questionPlaceholder: identity,
        knowledgeBaseNote: identity,
        askButton: startLabel,
        searchingMessage: identity,
        thinking: identity,
        emptyQuestion: identity,
        noAnswer: identity,
        requestError: identity,
        quotaExceeded: identity,
        voicePermission: identity,
        voiceNoSpeech: identity,
        voiceListening: identity,
        voiceReady: identity,
        voiceError: identity,
            sourcesHeading: label,
            noCitation: identity,
        footerText: identity
    };
});

const languageCodes = {
    English: "en", Assamese: "as", Bengali: "bn", Bodo: "brx", Dogri: "doi", Gujarati: "gu", Hindi: "hi", Kannada: "kn", Kashmiri: "ks", Konkani: "kok", Maithili: "mai", Malayalam: "ml", Manipuri: "mni", Marathi: "mr", Nepali: "ne", Odia: "or", Punjabi: "pa", Sanskrit: "sa", Santali: "sat", Sindhi: "sd", Tamil: "ta", Telugu: "te", Urdu: "ur"
};

const speechLocales = {
    English: "en-IN", Assamese: "as-IN", Bengali: "bn-IN", Bodo: "brx-IN", Dogri: "doi-IN", Gujarati: "gu-IN", Hindi: "hi-IN", Kannada: "kn-IN", Kashmiri: "ks-IN", Konkani: "kok-IN", Maithili: "mai-IN", Malayalam: "ml-IN", Manipuri: "mni-IN", Marathi: "mr-IN", Nepali: "ne-NP", Odia: "or-IN", Punjabi: "pa-IN", Sanskrit: "sa-IN", Santali: "sat-IN", Sindhi: "sd-IN", Tamil: "ta-IN", Telugu: "te-IN", Urdu: "ur-IN"
};

let selectedLanguage = document.getElementById("language").value;

function getTranslation(key) {
    const languageTranslation = translations[selectedLanguage] || translations.English;
    return languageTranslation[key] || translations.English[key] || key;
}

function updateInterface() {
    document.documentElement.lang = languageCodes[selectedLanguage] || "en";

    document.querySelectorAll("[data-i18n]").forEach(function (element) {
        element.innerHTML = getTranslation(element.dataset.i18n);
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (element) {
        element.placeholder = getTranslation(element.dataset.i18nPlaceholder);
    });

    const headerLanguage = document.querySelector(".header-language");
    if (headerLanguage) {
        headerLanguage.childNodes[0].textContent = getTranslation("languageLabel") + " ";
    }

    document.title = getTranslation("pageTitle");

    const ui = interfaceTranslations[selectedLanguage] || interfaceTranslations.English;
    const navLinks = document.querySelectorAll(".nav-link");
    const heroProof = document.querySelectorAll(".hero-proof span:not(.proof-line)");
    const signalCards = document.querySelectorAll(".signal-strip div");
    const topicButtons = document.querySelectorAll(".topic-pill");
    const guideCards = document.querySelectorAll(".guide-card");
    const absPoints = document.querySelectorAll(".abs-points span");

    navLinks.forEach(function (link, index) {
        link.textContent = ui.nav[index];
    });
    const headerAction = document.querySelector(".header-action");
    if (headerAction) {
        headerAction.innerHTML = ui.start;
    }
    document.querySelector(".hero-copy .eyebrow").childNodes[1].textContent = ui.heroEyebrow;
    document.querySelector(".hero h1").innerHTML = ui.heroTitle;
    document.querySelector(".hero-intro").textContent = ui.heroIntro;
    document.querySelector(".hero-actions .button").innerHTML = ui.ask;
    document.querySelector(".hero-actions .text-link").textContent = ui.explore;
    heroProof.forEach(function (element, index) {
        element.textContent = ui.proof[index];
    });
    const heroNotes = document.querySelectorAll(".hero-note strong, .hero-note small");
    if (heroNotes.length >= 4) {
        heroNotes[0].textContent = ui.heroNotes[0];
        heroNotes[1].textContent = ui.heroNotes[1];
        heroNotes[2].textContent = ui.heroNotes[2];
        heroNotes[3].textContent = ui.heroNotes[3];
    }
    const sealLabels = document.querySelectorAll(".hero-seal span");
    if (sealLabels.length >= 2) {
        sealLabels[0].textContent = ui.seal[0];
        sealLabels[1].textContent = ui.seal[1];
    }
    signalCards.forEach(function (card, index) {
        card.querySelector("span").textContent = ui.signals[index][0];
        card.querySelector("small").textContent = ui.signals[index][1];
    });

    const askHeading = document.querySelector("#ask .section-heading");
    askHeading.querySelector(".eyebrow").childNodes[0].textContent = ui.askEyebrow + " ";
    askHeading.querySelector("h2").innerHTML = ui.askTitle;
    askHeading.querySelector("p:last-child").textContent = ui.askText;
    document.querySelector(".topic-rail p").textContent = ui.lens;
    topicButtons.forEach(function (button, index) {
        button.textContent = ui.topics[index];
    });
    document.querySelector(".question-bottom span").textContent = getTranslation("knowledgeBaseNote");
    document.getElementById("askBtn").innerHTML = getTranslation("askButton") + " <span>→</span>";
    document.querySelector("#answerSection .panel-kicker").textContent = ui.response;
    document.querySelector("#answerSection h3").textContent = ui.answer;
    document.getElementById("clearBtn").textContent = ui.clear;

    const classification = document.querySelector("#classification");
    classification.querySelector(".eyebrow").childNodes[0].textContent = ui.classificationEyebrow + " ";
    classification.querySelector("h2").innerHTML = ui.classificationTitle;
    classification.querySelector(".section-lead").textContent = ui.classificationText;
    guideCards.forEach(function (card, index) {
        card.querySelector("h3").textContent = ui.cards[index][0];
        card.querySelector("p").textContent = ui.cards[index][1];
        card.querySelector("a").innerHTML = ui.cards[index][2].replace("↗", "<span>↗</span>");
    });

    const abs = document.querySelector("#abs");
    abs.querySelector(".eyebrow").childNodes[0].textContent = ui.absEyebrow + " ";
    abs.querySelector("h2").innerHTML = ui.absTitle;
    abs.querySelector(".section-heading > p").textContent = ui.absText;
    absPoints.forEach(function (point, index) {
        point.textContent = ui.absPoints[index];
    });
    abs.querySelector(".text-link").textContent = ui.absLink;

    const disclaimer = document.querySelector("#disclaimer");
    disclaimer.querySelector(".eyebrow").textContent = ui.disclaimerEyebrow;
    disclaimer.querySelector("h2").innerHTML = ui.disclaimerTitle;
    disclaimer.querySelector("div > p:last-child").textContent = ui.disclaimerText;

    const contact = document.querySelector("#contact");
    contact.querySelector(".eyebrow").textContent = ui.contactEyebrow;
    contact.querySelector("h2").innerHTML = ui.contactTitle;
    contact.querySelector(".contact-copy > p").textContent = ui.contactText;
    contact.querySelector(".button").innerHTML = ui.contactButton;
    contact.querySelector(".contact-card p").textContent = ui.contactCard;
    contact.querySelector(".contact-card small").textContent = ui.contactNote;
    document.querySelector(".footer-inner p").textContent = ui.footer;
    document.querySelector(".footer-inner > a").textContent = ui.top;
}

function setLoadingState(isLoading) {
    const loadingElement = document.getElementById("loading");
    if (!loadingElement) {
        return;
    }

    loadingElement.classList.toggle("visible", isLoading);
    loadingElement.classList.toggle("hidden", !isLoading);
}

async function askQuestion() {

    const questionInput = document.getElementById("question");
    const answer = document.getElementById("answer");
    const askButton = document.getElementById("askBtn");
    const question = questionInput.value.trim();

    if (question === "") {

        answer.innerText = getTranslation("emptyQuestion");

        return;
    }

    answer.innerText = getTranslation("thinking");
    setLoadingState(true);
    askButton.disabled = true;

    try {

        let response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question,
                language: selectedLanguage,
                topic: document.getElementById("topic").value
            })
        });

        const data = await response.json();

        if (!response.ok) {
            const error = new Error(data.answer || "The server could not answer the question.");
            error.code = data.error;
            error.status = response.status;
            throw error;
        }

        answer.innerText = data.answer || getTranslation("noAnswer");

        const sources = document.getElementById("sources");
        sources.innerHTML = "";
        const sourceHeading = document.createElement("strong");
        sourceHeading.textContent = getTranslation("sourcesHeading");
        sources.appendChild(sourceHeading);

        if (Array.isArray(data.sources) && data.sources.length > 0) {
            const sourceList = document.createElement("ul");
            data.sources.forEach(function (source) {
                const item = document.createElement("li");
                item.textContent = source;
                sourceList.appendChild(item);
            });
            sources.appendChild(sourceList);
        } else {
            const noCitation = document.createElement("p");
            noCitation.textContent = getTranslation("noCitation");
            sources.appendChild(noCitation);
        }

    } catch (error) {

        if (error.code === "insufficient_quota") {
            answer.innerText = "Your OpenAI account has no API credits remaining. Add billing credits, restart Flask, and try again.";
        } else if (error.status === 429 || error.code === "quota_exceeded") {
            answer.innerText = getTranslation("quotaExceeded");
        } else {
            answer.innerText = error.message || getTranslation("requestError");
        }
    } finally {
        askButton.disabled = false;
        setLoadingState(false);
    }
}

function clearChat() {
    document.getElementById("question").value = "";
    document.getElementById("answer").innerText = "";
    document.getElementById("sources").innerHTML = "";
    document.getElementById("askBtn").disabled = false;
    setLoadingState(false);
    document.getElementById("question").focus();
}

function initializeVoiceInput() {
    const questionInput = document.getElementById("question");
    if (!questionInput || document.getElementById("voiceBtn")) {
        return;
    }

    const wrapper = document.createElement("div");
    wrapper.className = "query-input-wrap";
    questionInput.parentNode.insertBefore(wrapper, questionInput);
    wrapper.appendChild(questionInput);

    const voiceButton = document.createElement("button");
    voiceButton.id = "voiceBtn";
    voiceButton.className = "voice-btn";
    voiceButton.type = "button";
    voiceButton.textContent = "🎙";
    voiceButton.setAttribute("aria-label", "Use voice input");
    voiceButton.title = "Use voice input";
    wrapper.appendChild(voiceButton);

    const status = document.createElement("p");
    status.id = "voiceStatus";
    status.className = "voice-status";
    status.setAttribute("aria-live", "polite");
    wrapper.parentNode.insertBefore(status, wrapper.nextSibling);

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        voiceButton.disabled = true;
        voiceButton.title = "Voice input is not supported in this browser";
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;
    recognition.lang = speechLocales[selectedLanguage] || "en-IN";
    let isListening = false;

    voiceButton.addEventListener("click", function () {
        if (isListening) {
            recognition.stop();
            return;
        }

        recognition.lang = speechLocales[selectedLanguage] || "en-IN";
        try {
            recognition.start();
            isListening = true;
            voiceButton.classList.add("recording");
            status.textContent = getTranslation("voiceListening");
        } catch (error) {
            isListening = false;
            status.textContent = getTranslation("voiceError");
        }
    });

    recognition.addEventListener("result", function (event) {
        const transcript = Array.from(event.results).map(function (result) {
            return result[0].transcript;
        }).join("");
        questionInput.value = transcript;
    });

    recognition.addEventListener("end", function () {
        isListening = false;
        voiceButton.classList.remove("recording");
        status.textContent = questionInput.value.trim() ? getTranslation("voiceReady") : "";
    });

    recognition.addEventListener("error", function (event) {
        isListening = false;
        voiceButton.classList.remove("recording");
        const messageKey = event.error === "not-allowed" || event.error === "service-not-allowed"
            ? "voicePermission"
            : event.error === "no-speech"
                ? "voiceNoSpeech"
                : "voiceError";
        status.textContent = getTranslation(messageKey);
    });
}

document.getElementById("askBtn").addEventListener("click", askQuestion);
document.getElementById("clearBtn").addEventListener("click", clearChat);

document.getElementById("contactToggle").addEventListener("click", function () {
    const details = document.getElementById("contactDetails");
    const isOpen = details.hasAttribute("hidden");
    details.toggleAttribute("hidden", !isOpen);
    this.setAttribute("aria-expanded", String(isOpen));
});

document.querySelectorAll(".topic-pill").forEach(function (button) {
    button.addEventListener("click", function () {
        document.querySelectorAll(".topic-pill").forEach(function (topicButton) {
            topicButton.classList.remove("selected");
        });
        button.classList.add("selected");
        document.getElementById("topic").value = button.dataset.topic;
    });
});

document.querySelectorAll("[data-topic-link]").forEach(function (link) {
    link.addEventListener("click", function () {
        const topic = link.dataset.topicLink;
        document.querySelectorAll(".topic-pill").forEach(function (topicButton) {
            topicButton.classList.toggle("selected", topicButton.dataset.topic === topic);
        });
        document.getElementById("topic").value = topic;
    });
});

const menuToggle = document.getElementById("menuToggle");
const siteNav = document.getElementById("siteNav");

menuToggle.addEventListener("click", function () {
    const isOpen = siteNav.classList.toggle("open");
    menuToggle.setAttribute("aria-expanded", String(isOpen));
});

siteNav.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
        siteNav.classList.remove("open");
        menuToggle.setAttribute("aria-expanded", "false");
    });
});

const navigationLinks = document.querySelectorAll(".nav-link");
const pageSections = document.querySelectorAll("main section[id]");
const homeSupport = document.querySelector(".home-support, .signal-strip");
pageSections.forEach(function (section) {
    section.classList.add("page-section");
});

document.querySelectorAll(".signal-strip div").forEach(function (card, index) {
    const destinations = ["ask", "classification", "abs"];
    card.setAttribute("role", "button");
    card.setAttribute("tabindex", "0");
    card.addEventListener("click", function () {
        showSection(destinations[index], true);
        history.replaceState(null, "", "#" + destinations[index]);
    });
    card.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            card.click();
        }
    });
});

function showSection(sectionId, shouldFocus) {
    const targetSection = document.getElementById(sectionId) || document.getElementById("home");

    pageSections.forEach(function (section) {
        section.classList.toggle("active-section", section === targetSection);
    });

    if (homeSupport) {
        homeSupport.classList.toggle("hidden-view", targetSection.id !== "home");
    }

    navigationLinks.forEach(function (link) {
        link.classList.toggle("active", link.getAttribute("href") === "#" + targetSection.id);
    });

    if (shouldFocus) {
        targetSection.focus({ preventScroll: true });
        window.scrollTo({ top: 0, behavior: "smooth" });
    }
}

document.querySelectorAll("a[href^='#']").forEach(function (link) {
    link.addEventListener("click", function (event) {
        const targetId = link.getAttribute("href").slice(1);
        if (document.getElementById(targetId)) {
            event.preventDefault();
            showSection(targetId, true);
            history.replaceState(null, "", "#" + targetId);
        }
    });
});

showSection(window.location.hash.slice(1) || "home", false);

document.getElementById("language").addEventListener("change", function (event) {
    selectedLanguage = event.target.value;
    updateInterface();
});

document.getElementById("question").addEventListener("keydown", function (event) {
    if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
        event.preventDefault();
        askQuestion();
    }
});

initializeVoiceInput();
updateInterface();