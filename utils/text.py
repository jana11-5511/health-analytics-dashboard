"""Text formatting helpers."""


def clean_cause_name(col: str) -> str:
    name = col.replace("Deaths - ", "")
    return name.split(" - Sex")[0].split(" (Rate")[0].strip()


def wrap_title(text: str, width: int = 22) -> str:
    words = text.split()
    lines, line, cur = [], [], 0
    for w in words:
        add = len(w) + (1 if line else 0)
        if cur + add <= width:
            line.append(w); cur += add
        else:
            if line: lines.append(" ".join(line))
            line, cur = [w], len(w)
    if line: lines.append(" ".join(line))
    return "<br>".join(lines)


_CATEGORY_RULES = (
    ('Salud mental/Adicciones',  ['mental', 'drug use', 'alcohol use', 'substance', 'self-harm',
                                  'suicide', 'depressive', 'schizophrenia', 'bipolar', 'anxiety',
                                  'eating disorder']),
    ('Lesiones externas',        ['injury', 'accident', 'violence', 'conflict', 'terrorism', 'road',
                                  'drowning', 'fire', 'fall', 'poisoning', 'war', 'homicide',
                                  'interpersonal', 'environmental heat']),
    ('Infecciosas',              ['hiv', 'aids', 'tuberculosis', 'malaria', 'diarrheal', 'meningitis',
                                  'hepatitis', 'typhoid', 'cholera', 'measles', 'pertussis', 'sepsis',
                                  'lower respiratory', 'respiratory infection', 'enteric',
                                  'intestinal infectious', 'infectious']),
    ('Cardiovascular/Metabólicas', ['cardiovascular', 'diabetes', 'kidney', 'ischemic', 'stroke',
                                    'hypertensive', 'heart', 'atrial fibrillation', 'peripheral vascular',
                                    'rheumatic', 'endocarditis', 'metabolic']),
    ('Cáncer',                   ['neoplasm', 'cancer', 'tumor', 'carcinoma', 'leukemia', 'lymphoma',
                                  'mesothelioma', 'sarcoma']),
    ('Materno-infantil',         ['maternal', 'neonatal', 'nutritional', 'protein-energy', 'vitamin',
                                  'iron-deficiency', 'malnutrition']),
    ('Enf. crónicas',            ['chronic', 'copd', 'asthma', 'pneumoconiosis', 'alzheimer', 'parkinson',
                                  'dementia', 'epilepsy', 'multiple sclerosis', 'neurological',
                                  'digestive', 'musculoskeletal', 'cirrhosis', 'peptic ulcer',
                                  'inflammatory bowel', 'respiratory']),
)


def categorize_cause(cause_name: str) -> str:
    c = cause_name.lower()
    for label, keywords in _CATEGORY_RULES:
        if any(k in c for k in keywords):
            return label
    return 'Otras'