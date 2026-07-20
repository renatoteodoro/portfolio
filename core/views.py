"""
Views do portfolio de Renato Teodoro.
Os dados (projetos, skills, experiencias) sao definidos diretamente aqui
como listas de dicionarios, sem necessidade de banco de dados.
"""

import json
import logging
import os
import re

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Base de conhecimento para o chatbot
# ---------------------------------------------------------------------------

KNOWLEDGE_BASE = """
SOBRE RENATO TEODORO:
Nome: Renato Teodoro
Nascimento: 23 de maio de 1982
Localização: Palhoça/SC – Brasil
Email: renatoteodoro2@gmail.com
Telefone: (48) 99640-4676

PERFIL:
Profissional com mais de 25 anos de experiência em eletrônica, telecomunicações, segurança eletrônica e TI.
Em transição complementar para desenvolvimento de software. Stack principal: Python, Django, DRF, LangChain, OpenAI API, RAG, Agentes de IA, PostgreSQL, AWS, Git.

EXPERIÊNCIAS:
1. Intelbras S/A (Jun/2025–Maio/2026): Analista de Treinamento Técnico Pleno. Desenvolvimento trilhas EAD/presencial para BU-SEG, conteúdos humanizados, gestão instrutores.
2. Claro Brasil (Mai/2023–Jun/2025): Técnico IAT I. Manutenção HFC/GPON, configuração redes, SLA.
3. Autônomo (Jul/2020–Abr/2023): Empreendedor em segurança eletrônica e elétrica. CFTV, alarmes, controle de acesso. Participou do Programa Nascer de Pré-Incubação (FAPESC + SCTI + SEBRAE/SC — VI Edição 2025) com o projeto AccessFive — projeto de IA para segurança industrial: detecção de EPIs e zonas de risco em tempo real usando câmeras CCTV e IoT existentes, análise preditiva e alertas imediatos ao supervisor.
4. Ezentis Brasil (Jan/2018–Jul/2020): Técnico Telecom. Torres celulares TIM 2G/3G/4G, NR10, NR35.
5. FIESC-SENAI (Ago/2012–Dez/2016): Coordenador/Professor. PRONATEC, cursos elétrica/eletrônica/telecom.
6. Dígitro Tecnologia (Nov/2005–Ago/2012): Técnico Eletrônica. Suporte engenharia, projetos energia solar.

PROJETOS DE SOFTWARE:
1. Portfólio: Django 5, Tailwind CSS, OpenAI GPT-4o-mini, WhiteNoise, Python, JavaScript. Site portfólio profissional com chatbot de IA integrado, dark/light mode, timeline de experiências com fotos reais e formulário de contato via SMTP. Em produção (portfolio-renato.fly.dev).
2. Beton Dekor: Django 6.0, htmx, Cloudinary, PostgreSQL, Docker, Gunicorn. Site institucional com catálogo de produtos para empresa de revestimentos decorativos, replicando layout Figma. Galeria com Cloudinary, formulário de contato SMTP, responsivo. Em produção na Hostinger (betondekor.com.br).
3. EnergIA: Django 5, PostgreSQL/TimescaleDB, MQTT, DRF, scikit-learn, LangChain, Flet, Docker. Plataforma IoT de monitoramento de consumo de energia elétrica: ingestão MQTT, forecasting de fatura e NILM, assistente WhatsApp via LangChain/RAG, API REST alimentando app mobile em Flet. Em produção (energiasm.online); resultado preliminar admissível no Programa Nascer FAPESC 2026.
4. PlannerEdu: Django 5.2, PostgreSQL, Docker, Chart.js, SortableJS, Bootstrap 5. Plataforma de gestão de produção educacional com calendário anual, dashboard analítico com KPIs, Kanban drag-and-drop e sistema multi-usuário com permissões. Sem deploy ativo no momento (código completo no GitHub).
5. ADA: Django, OpenAI GPT-4o-mini, Whisper (STT), TTS, Playwright, ReportLab. Assistente virtual multi-modal desenvolvido no Hackathon 2025 (Jovem Programador — Senac/SC). Voz bidirecional, acessibilidade com VLibras, painel admin com exportação CSV/Excel/PDF. Deploy pausado atualmente (custos AWS).
6. WathsBotApp: FastAPI, LangChain, OpenAI, ChromaDB, Redis, Evolution API, Playwright, Docker. Assistente RAG para WhatsApp com debounce inteligente, memória de sessão via Redis, scraping automático de base de conhecimento a cada 30 dias. Sem deploy público (código no GitHub).

EMPREENDEDORISMO E INOVAÇÃO:
1. Programa Nascer 2025 (FAPESC + SEBRAE/SC — VI Edição): pré-incubação de ideias inovadoras do ecossistema catarinense. Projeto: AccessFive — "Inteligência Artificial a Serviço da Segurança Industrial", projeto que usa câmeras CCTV e sensores IoT já existentes nas empresas para detectar automaticamente o não-uso de EPIs e zonas de risco em tempo real, disparando alertas imediatos ao supervisor. Mercado: 623 mil acidentes/ano no Brasil, 2.583 mortes em 2024, R$ 115 bilhões em custos anuais; setor de IA para segurança cresce 28,5%/ano, alcançando US$ 38 bilhões até 2035.
2. Programa Nascer 2026 (FAPESC — VII Edição, Edital 024/2026, polo Florianópolis, resultado preliminar admissível): mesma pré-incubação, agora com o projeto EnergIA — Smart Meter, plataforma IoT de monitoramento e análise de consumo de energia elétrica.
3. Hackathon Tech Floripa 2026 — 1ª Jornada Incubintech (promovido pelo Incubintech/IFSC, com apoio da Receita Federal e do poder público): Renato compete com o EnergIA no Desafio 6 — Medidor como Assistente de Energia. Em andamento, fase final em 25/07/2026 em Florianópolis.
4. Beton Dekor: projeto de desenvolvimento autônomo/freelance — captação de cliente, projeto do zero e deploy em produção, sem vínculo com programa de fomento.

FORMAÇÃO:
- Especialização Computação Científica para a Indústria – IFSC (em andamento)
- Tecnólogo Sistemas para Internet – Estácio de Sá (concluído)
- Técnico em Eletrônica – SENAI (2007)

CERTIFICAÇÕES:
- PycodeBR Python Master: Python, Django, DRF, OpenAI/LangChain, AWS, Mercado Pago — 100h+, 450+ aulas
- NR10 – Segurança em Eletricidade
- NR35 – Trabalho em Altura

SKILLS TÉCNICAS:
Backend: Python (90%), Django (85%), DRF (80%), FastAPI (65%)
IA/ML: LangChain (75%), OpenAI API (80%), RAG (70%), Agentes de IA (65%)
Database: PostgreSQL (80%), SQLite (90%), Redis (55%)
DevOps: AWS EC2/S3 (60%), Docker (65%), Git/GitHub (85%), Railway/Render (70%)
Frontend: HTML5/CSS3 (80%), Tailwind CSS (75%), JavaScript (60%)
Hardware/IoT: Arduino (85%), ESP32 (80%), MQTT (75%), C/C++ (70%)
"""

# ---------------------------------------------------------------------------
# Dados do portfolio
# ---------------------------------------------------------------------------

PROJETOS = [
    {
        'id': 1,
        'titulo': 'Portfólio — Site Pessoal com Chatbot IA',
        'descricao': (
            'Site portfólio profissional desenvolvido com Django 5, Tailwind CSS e chatbot de IA '
            'integrado. O assistente usa OpenAI GPT-4o-mini quando disponível, com fallback por '
            'palavras-chave. Dark/light mode persistente, seções de projetos, timeline de '
            'experiências com fotos reais e formulário de contato via SMTP.'
        ),
        'stack': ['Django 5', 'Tailwind CSS', 'OpenAI GPT-4o-mini', 'WhiteNoise', 'Python', 'JavaScript'],
        'stack_cores': {
            'Django 5': 'bg-green-700',
            'Tailwind CSS': 'bg-teal-700',
            'OpenAI GPT-4o-mini': 'bg-slate-600',
            'WhiteNoise': 'bg-blue-800',
            'Python': 'bg-blue-700',
            'JavaScript': 'bg-yellow-700',
        },
        'github_url': 'https://github.com/renatoteodoro/portfolio',
        'demo_url': 'https://portfolio-renato.fly.dev/',
        'destaque': True,
        'icone': 'fa-briefcase',
    },
    {
        'id': 2,
        'titulo': 'Beton Dekor — Site Institucional',
        'descricao': (
            'Site institucional com catálogo de produtos para empresa de revestimentos decorativos, '
            'replicando fielmente o layout Figma. Galeria de imagens com Cloudinary, '
            'formulário de contato com SMTP, interfaces responsivas (mobile, tablet, desktop) '
            'e deploy em produção na Hostinger com Docker e Gunicorn.'
        ),
        'stack': ['Django 6.0', 'htmx', 'Cloudinary', 'PostgreSQL', 'Docker', 'Gunicorn', 'WhiteNoise'],
        'stack_cores': {
            'Django 6.0': 'bg-green-700',
            'htmx': 'bg-blue-600',
            'Cloudinary': 'bg-indigo-700',
            'PostgreSQL': 'bg-blue-800',
            'Docker': 'bg-blue-700',
            'Gunicorn': 'bg-green-800',
            'WhiteNoise': 'bg-slate-600',
        },
        'github_url': 'https://github.com/renatoteodoro/beton-dekor-deploy',
        'demo_url': 'https://www.betondekor.com.br/',
        'destaque': False,
        'icone': 'fa-store',
    },
    {
        'id': 3,
        'titulo': 'EnergIA — Plataforma IoT de Monitoramento de Energia',
        'descricao': (
            'Plataforma IoT completa de monitoramento e análise de consumo de energia elétrica. '
            'Django 5 full-stack com 9 apps desacoplados, TimescaleDB para séries temporais de '
            'telemetria (hypertables), ingestão via MQTT, forecasting de fatura e NILM com '
            'scikit-learn, e assistente WhatsApp com LangChain/RAG. API REST (DRF) alimenta '
            'um app mobile em Flet.'
        ),
        'stack': ['Django 5', 'PostgreSQL + TimescaleDB', 'MQTT', 'DRF', 'scikit-learn', 'LangChain', 'Flet', 'Docker'],
        'stack_cores': {
            'Django 5': 'bg-green-700',
            'PostgreSQL + TimescaleDB': 'bg-blue-800',
            'MQTT': 'bg-purple-700',
            'DRF': 'bg-teal-700',
            'scikit-learn': 'bg-orange-700',
            'LangChain': 'bg-green-800',
            'Flet': 'bg-cyan-700',
            'Docker': 'bg-blue-700',
        },
        'github_url': 'https://github.com/renatoteodoro/EnergIA',
        'demo_url': 'https://energiasm.online',
        'destaque': True,
        'icone': 'fa-bolt',
    },
    {
        'id': 4,
        'titulo': 'PlannerEdu — Gestão de Produção Educacional',
        'descricao': (
            'Plataforma web completa para planejamento anual de produção de conteúdo educacional. '
            'Calendário interativo com feriados brasileiros, dashboard analítico com KPIs e '
            'gráficos (Chart.js), sistema Kanban drag-and-drop para cursos EAD/presencial '
            'e controle multi-usuário com permissões granulares. Deploy previsto na IONOS com Docker.'
        ),
        'stack': ['Django 5.2', 'PostgreSQL', 'Docker', 'Chart.js', 'SortableJS', 'Bootstrap 5', 'IONOS'],
        'stack_cores': {
            'Django 5.2': 'bg-green-700',
            'PostgreSQL': 'bg-blue-800',
            'Docker': 'bg-blue-700',
            'Chart.js': 'bg-pink-700',
            'SortableJS': 'bg-yellow-700',
            'Bootstrap 5': 'bg-purple-700',
            'IONOS': 'bg-red-700',
        },
        'github_url': 'https://github.com/renatoteodoro/planner_edu',
        'demo_url': '',
        'destaque': False,
        'icone': 'fa-calendar-check',
    },
    {
        'id': 5,
        'titulo': 'ADA — Assistente Virtual Multi-modal',
        'descricao': (
            'Assistente conversacional com IA desenvolvido no Hackathon 2025 (Jovem Programador — Senac/SC). '
            'Suporte a voz bidirecional via Whisper (STT) e TTS, '
            'acessibilidade com VLibras (Libras), scraping automático com Playwright, '
            'e painel administrativo com exportação em CSV, Excel e PDF.'
        ),
        'stack': ['Django', 'OpenAI GPT-4o-mini', 'Whisper', 'TTS', 'Playwright', 'ReportLab', 'AWS'],
        'stack_cores': {
            'Django': 'bg-green-700',
            'OpenAI GPT-4o-mini': 'bg-slate-600',
            'Whisper': 'bg-orange-700',
            'TTS': 'bg-yellow-700',
            'Playwright': 'bg-indigo-700',
            'ReportLab': 'bg-red-700',
            'AWS': 'bg-amber-700',
        },
        'github_url': 'https://github.com/renatoteodoro/ADA',
        'demo_url': '',
        'nota_deploy': 'Deploy pausado — custos AWS',
        'destaque': True,
        'icone': 'fa-microphone',
    },
    {
        'id': 6,
        'titulo': 'WathsBotApp — Assistente RAG para WhatsApp',
        'descricao': (
            'Assistente virtual para WhatsApp com RAG conversacional baseado em dados '
            'reais extraídos via Playwright (web scraping). Debounce inteligente agrupa '
            'mensagens picadas antes de processar. Memória de sessão via Redis e '
            'atualização autônoma da base vetorial a cada 30 dias.'
        ),
        'stack': ['FastAPI', 'LangChain', 'OpenAI', 'ChromaDB', 'Redis', 'Evolution API', 'Playwright', 'Docker'],
        'stack_cores': {
            'FastAPI': 'bg-teal-700',
            'LangChain': 'bg-green-700',
            'OpenAI': 'bg-slate-600',
            'ChromaDB': 'bg-purple-700',
            'Redis': 'bg-red-700',
            'Evolution API': 'bg-green-800',
            'Playwright': 'bg-indigo-700',
            'Docker': 'bg-blue-800',
        },
        'github_url': 'https://github.com/renatoteodoro/WathsBotApp',
        'demo_url': '',
        'destaque': False,
        'icone': 'fa-comments',
    },
]

SKILLS = [
    {
        'categoria': 'Backend',
        'icone': 'fa-server',
        'cor': 'text-blue-400',
        'tecnologias': [
            {'nome': 'Python', 'nivel': 90},
            {'nome': 'Django', 'nivel': 85},
            {'nome': 'Django REST Framework', 'nivel': 80},
            {'nome': 'FastAPI', 'nivel': 65},
        ],
    },
    {
        'categoria': 'IA / Machine Learning',
        'icone': 'fa-brain',
        'cor': 'text-purple-400',
        'tecnologias': [
            {'nome': 'LangChain', 'nivel': 75},
            {'nome': 'OpenAI API', 'nivel': 80},
            {'nome': 'RAG', 'nivel': 70},
            {'nome': 'Agentes de IA', 'nivel': 65},
        ],
    },
    {
        'categoria': 'Database',
        'icone': 'fa-database',
        'cor': 'text-green-400',
        'tecnologias': [
            {'nome': 'PostgreSQL', 'nivel': 80},
            {'nome': 'SQLite', 'nivel': 90},
            {'nome': 'Redis', 'nivel': 55},
        ],
    },
    {
        'categoria': 'DevOps & Cloud',
        'icone': 'fa-cloud',
        'cor': 'text-orange-400',
        'tecnologias': [
            {'nome': 'AWS (EC2, S3)', 'nivel': 60},
            {'nome': 'Docker', 'nivel': 65},
            {'nome': 'Git / GitHub', 'nivel': 85},
            {'nome': 'Railway / Render', 'nivel': 70},
        ],
    },
    {
        'categoria': 'Frontend',
        'icone': 'fa-code',
        'cor': 'text-cyan-400',
        'tecnologias': [
            {'nome': 'HTML5 / CSS3', 'nivel': 80},
            {'nome': 'Tailwind CSS', 'nivel': 75},
            {'nome': 'JavaScript', 'nivel': 60},
        ],
    },
    {
        'categoria': 'Hardware / IoT',
        'icone': 'fa-microchip',
        'cor': 'text-yellow-400',
        'tecnologias': [
            {'nome': 'Arduino', 'nivel': 85},
            {'nome': 'ESP32', 'nivel': 80},
            {'nome': 'MQTT', 'nivel': 75},
            {'nome': 'C / C++', 'nivel': 70},
        ],
    },
]

EXPERIENCIAS = [
    {
        'cargo': 'Analista de Treinamento Técnico Pleno',
        'empresa': 'INTELBRAS S/A',
        'periodo': 'Jun/2025 – Maio/2026',
        'descricao': (
            'Desenvolvimento de trilhas de treinamento EAD e presencial para a unidade de '
            'Segurança Eletrônica (BU-SEG). Criação de conteúdos humanizados com gravações '
            'em estúdio profissional, gestão de instrutores e alinhamento contínuo do '
            'treinamento às demandas do mercado de segurança eletrônica.'
        ),
        'tecnologias': ['EAD', 'Instrução Técnica', 'Segurança Eletrônica', 'Gestão de Treinamento'],
        'foto': 'core/images/exp/intelbras.png',
        'icone': 'fa-building',
        'cor_borda': 'border-blue-500',
        'cor_icone': 'bg-blue-500',
    },
    {
        'cargo': 'Técnico IAT I',
        'empresa': 'CLARO BRASIL SA',
        'periodo': 'Mai/2023 – Jun/2025',
        'descricao': (
            'Manutenção preventiva e corretiva em redes HFC e GPON, configuração de modems, '
            'roteadores mesh e decoders. Atendimento com foco em SLA, cumprimento de metas '
            'diárias e qualidade no atendimento ao cliente final.'
        ),
        'tecnologias': ['HFC', 'GPON', 'Redes', 'Modems', 'SLA', 'Fibra Óptica'],
        'foto': 'core/images/exp/claro.jpg',
        'icone': 'fa-wifi',
        'cor_borda': 'border-red-500',
        'cor_icone': 'bg-red-500',
    },
    {
        'cargo': 'Empreendedor – Segurança Eletrônica e Elétrica',
        'empresa': 'Autônomo',
        'periodo': 'Jul/2020 – Abr/2023',
        'descricao': (
            'Prestação de serviços em CFTV, alarmes, controle de acesso, telecomunicações e '
            'instalações elétricas industriais e prediais. Participou do Programa Nascer de '
            'Pré-Incubação (FAPESC + SEBRAE/SC — VI Edição 2025) com o projeto AccessFive — '
            'projeto de IA para detecção de EPIs e zonas de risco em ambientes industriais.'
        ),
        'tecnologias': ['CFTV', 'Alarmes', 'Controle de Acesso', 'Elétrica Industrial', 'Empreendedorismo'],
        'foto': 'core/images/exp/autonomo.jpg',
        'icone': 'fa-shield-halved',
        'cor_borda': 'border-yellow-500',
        'cor_icone': 'bg-yellow-600',
    },
    {
        'cargo': 'Técnico em Telecomunicações',
        'empresa': 'EZENTIS BRASIL SA',
        'periodo': 'Jan/2018 – Jul/2020',
        'descricao': (
            'Manutenção preventiva e corretiva em torres de telefonia celular TIM 2G/3G/4G '
            'com equipamentos Huawei e SIAE. Trabalho em altura com NR10 e NR35, garantindo '
            'a integridade e disponibilidade da infraestrutura de telecomunicações.'
        ),
        'tecnologias': ['Telecom', '4G/3G/2G', 'Huawei', 'SIAE', 'NR10', 'NR35', 'Torres'],
        'foto': 'core/images/exp/ezentis.jpg',
        'icone': 'fa-tower-broadcast',
        'cor_borda': 'border-green-500',
        'cor_icone': 'bg-green-600',
    },
    {
        'cargo': 'Coordenador de Curso / Professor',
        'empresa': 'FIESC – SENAI',
        'periodo': 'Ago/2012 – Dez/2016',
        'descricao': (
            'Coordenação e docência em cursos técnicos de Eletrotécnica e Eletrônica no '
            'programa PRONATEC e cursos de Aprendizagem Industrial. Desenvolvimento de '
            'material didático, acompanhamento pedagógico e formação de profissionais '
            'para o setor industrial.'
        ),
        'tecnologias': ['Docência', 'PRONATEC', 'Eletrotécnica', 'Eletrônica', 'Coordenação'],
        'foto': 'core/images/exp/senai1.jpg',
        'foto2': 'core/images/exp/senai2.jpg',
        'icone': 'fa-graduation-cap',
        'cor_borda': 'border-orange-500',
        'cor_icone': 'bg-orange-500',
    },
    {
        'cargo': 'Técnico em Eletrônica',
        'empresa': 'Dígitro Tecnologia',
        'periodo': 'Nov/2005 – Ago/2012',
        'descricao': (
            'Suporte à engenharia de produção, inspeção, testes e homologação de equipamentos '
            'eletrônicos. Participação em projetos de energia solar fotovoltaica e '
            'desenvolvimento de protótipos para soluções de telecomunicações.'
        ),
        'tecnologias': ['Eletrônica', 'Testes', 'Homologação', 'Energia Solar', 'P&D'],
        'foto': None,
        'icone': 'fa-circuit-board',
        'cor_borda': 'border-purple-500',
        'cor_icone': 'bg-purple-600',
    },
    {
        'cargo': 'Experiências Anteriores',
        'empresa': 'Mondiana / Policast / Eportel',
        'periodo': '1998 – 2005',
        'descricao': (
            'Mondiana Ind. Plásticos (2005): produção industrial. '
            'Policast Ind. e Comércio (2001–2005): manutenção industrial. '
            'Eportel Com. Mat. Elétricos (1998–2000): comércio de materiais elétricos, '
            'atendimento técnico e suporte a clientes do setor de construção civil.'
        ),
        'tecnologias': ['Elétrica', 'Manutenção Industrial', 'Comércio Técnico'],
        'foto': None,
        'icone': 'fa-briefcase',
        'cor_borda': 'border-slate-500',
        'cor_icone': 'bg-slate-600',
    },
]

EMPREENDEDORISMO = [
    {
        'titulo': 'Programa Nascer 2025',
        'badge': 'FAPESC + SEBRAE/SC · VI Edição',
        'descricao': (
            'Pré-incubação de ideias inovadoras do ecossistema catarinense de inovação. '
            'Participação com o projeto AccessFive — IA para segurança industrial, detectando '
            'EPIs e zonas de risco em tempo real via câmeras CCTV e sensores IoT existentes.'
        ),
        'projeto': 'AccessFive',
        'icone': 'fa-shield-halved',
        'cor_gradiente': 'from-blue-500 to-purple-600',
    },
    {
        'titulo': 'Programa Nascer 2026',
        'badge': 'FAPESC · VII Edição · Resultado preliminar',
        'descricao': (
            'Nova edição do mesmo programa de pré-incubação (Edital FAPESC N.º 024/2026), polo '
            'Florianópolis. Participação com o projeto EnergIA — Smart Meter, plataforma IoT de '
            'monitoramento e análise de consumo de energia elétrica.'
        ),
        'projeto': 'EnergIA',
        'icone': 'fa-bolt',
        'cor_gradiente': 'from-emerald-500 to-cyan-500',
    },
    {
        'titulo': 'Hackathon Tech Floripa 2026',
        'badge': '1ª Jornada Incubintech · IFSC · Em andamento',
        'descricao': (
            'Hackathon de inovação aberta promovido pelo Incubintech (IFSC), com apoio da '
            'Receita Federal e do poder público. Competindo com o EnergIA no Desafio 6 — '
            'Medidor como Assistente de Energia. Fase final em 25/07/2026, em Florianópolis.'
        ),
        'projeto': 'EnergIA',
        'icone': 'fa-trophy',
        'cor_gradiente': 'from-amber-500 to-orange-600',
    },
    {
        'titulo': 'Beton Dekor',
        'badge': 'Projeto autônomo / freelance',
        'descricao': (
            'Desenvolvimento independente de site institucional para empresa de revestimentos '
            'decorativos: captação do cliente, projeto do zero e deploy em produção, sem '
            'vínculo com programa de fomento.'
        ),
        'projeto': 'Beton Dekor',
        'icone': 'fa-store',
        'cor_gradiente': 'from-slate-500 to-slate-700',
    },
]


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

def index(request):
    """Renderiza a pagina principal do portfolio com todas as secoes."""
    context = {
        'projetos': PROJETOS,
        'skills': SKILLS,
        'experiencias': EXPERIENCIAS,
        'empreendedorismo': EMPREENDEDORISMO,
        'stack_principal': [
            'Python', 'Django', 'DRF', 'LangChain',
            'OpenAI', 'RAG', 'PostgreSQL', 'AWS', 'Git', 'ESP32',
        ],
    }
    return render(request, 'core/index.html', context)


def contato(request):
    """Processa o formulario de contato e envia email."""
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        assunto = request.POST.get('assunto', '').strip()
        mensagem_texto = request.POST.get('mensagem', '').strip()

        if not all([nome, email, assunto, mensagem_texto]):
            messages.error(request, 'Por favor, preencha todos os campos.')
            return redirect('index')

        corpo_email = (
            f'Nome: {nome}\n'
            f'Email: {email}\n'
            f'Assunto: {assunto}\n\n'
            f'Mensagem:\n{mensagem_texto}'
        )

        try:
            send_mail(
                subject=f'[Portfolio] {assunto} - de {nome}',
                message=corpo_email,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['renatoteodoro2@gmail.com'],
                fail_silently=False,
            )
            logger.info('Email de contato enviado de: %s', email)
            messages.success(
                request,
                'Mensagem enviada com sucesso! Responderei em breve.'
            )
        except Exception as exc:
            logger.error('Falha ao enviar email de contato: %s', exc)
            messages.error(
                request,
                'Ocorreu um erro ao enviar a mensagem. Tente novamente ou entre em contato diretamente pelo email.'
            )

        return redirect('index')

    return redirect('index')


@require_POST
@csrf_exempt
def chatbot(request):
    """Endpoint do chatbot do portfolio. Usa OpenAI se disponivel, senao fallback por palavras-chave."""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        if not user_message:
            return JsonResponse({'response': 'Por favor, faça uma pergunta sobre o portfólio ou currículo do Renato.'})

        openai_key = os.environ.get('OPENAI_API_KEY', '') or getattr(settings, 'OPENAI_API_KEY', '')

        if openai_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)
                response = client.chat.completions.create(
                    model='gpt-4o-mini',
                    messages=[
                        {
                            'role': 'system',
                            'content': (
                                'Você é um assistente do portfólio profissional de Renato Teodoro. '
                                'Responda APENAS perguntas sobre o portfólio e currículo do Renato usando as informações abaixo. '
                                'Se perguntarem sobre outros assuntos, redirecione educadamente para o tema do portfólio. '
                                'Responda em português, de forma profissional e amigável.\n\n'
                                f'BASE DE CONHECIMENTO:\n{KNOWLEDGE_BASE}'
                            ),
                        },
                        {'role': 'user', 'content': user_message},
                    ],
                    max_tokens=500,
                    temperature=0.7,
                )
                bot_response = response.choices[0].message.content
                return JsonResponse({'response': bot_response})
            except Exception as exc:
                logger.warning('OpenAI falhou, usando fallback: %s', exc)

        bot_response = _keyword_response(user_message)
        return JsonResponse({'response': bot_response})

    except Exception as exc:
        logger.error('Erro no chatbot: %s', exc)
        return JsonResponse({'response': 'Desculpe, ocorreu um erro. Tente novamente.'}, status=500)


def _keyword_response(message: str) -> str:
    """Gera resposta baseada em palavras-chave quando OpenAI nao esta disponivel."""
    msg = message.lower()

    if any(w in msg for w in ['experiência', 'experiencia', 'trabalhou', 'empresa', 'carreira', 'histórico']):
        return (
            'Renato tem 25+ anos de experiência profissional. Trabalhou na Intelbras (Analista de Treinamento), '
            'Claro Brasil (Técnico IAT), atuou como autônomo em segurança eletrônica (onde participou do '
            'Programa Nascer com o projeto AccessFive — IA para segurança industrial), Ezentis Brasil (torres celulares), FIESC-SENAI '
            '(professor/coordenador) e Dígitro Tecnologia (técnico eletrônica).'
        )

    if any(w in msg for w in ['intelbras']):
        return (
            'Na Intelbras S/A (Jun/2025–Maio/2026), Renato atuou como Analista de Treinamento Técnico Pleno, '
            'desenvolvendo trilhas de treinamento EAD e presencial para a unidade de Segurança Eletrônica (BU-SEG), '
            'criando conteúdos humanizados com gravações em estúdio.'
        )

    if any(w in msg for w in ['claro', 'telefonia', 'hfc', 'gpon']):
        return (
            'Na Claro Brasil (Mai/2023–Jun/2025), Renato trabalhou como Técnico IAT I, realizando manutenção '
            'preventiva e corretiva em redes HFC e GPON, configurando modems, roteadores mesh e decoders, '
            'garantindo SLA nas manutenções.'
        )

    if any(w in msg for w in ['nascer', 'accessfive', 'access five', 'startup', 'sebrae', 'fapesc', 'empreendedor', 'epi', 'segurança industrial', 'seguranca industrial', 'hackathon', 'incubintech', 'tech floripa', 'beton dekor']):
        return (
            'Renato tem 4 frentes de empreendedorismo e inovação: '
            '(1) Programa Nascer 2025 (FAPESC + SEBRAE/SC) com o AccessFive — IA para detecção de EPIs e '
            'zonas de risco industrial via CCTV/IoT; '
            '(2) Programa Nascer 2026 (FAPESC, resultado preliminar) com o EnergIA — plataforma IoT de '
            'monitoramento de energia; '
            '(3) Hackathon Tech Floripa 2026 — 1ª Jornada Incubintech (IFSC), competindo com o EnergIA no '
            'Desafio 6 (Medidor como Assistente de Energia), em andamento até 25/07/2026; '
            '(4) Beton Dekor — projeto autônomo/freelance, do zero ao deploy em produção.'
        )

    if any(w in msg for w in ['projeto', 'projetos', 'software', 'sistema']):
        return (
            'Renato desenvolveu 6 projetos principais: '
            '(1) Portfólio — site pessoal com chatbot de IA, dark/light mode e timeline de experiências '
            '(Django 5, Tailwind CSS), em produção; '
            '(2) Beton Dekor — site institucional com catálogo Cloudinary, em produção na Hostinger (Django 6); '
            '(3) EnergIA — plataforma IoT de monitoramento de energia com TimescaleDB, MQTT e forecasting via '
            'scikit-learn, em produção; '
            '(4) PlannerEdu — plataforma Django de gestão educacional com Kanban e dashboard analítico, '
            'código no GitHub; '
            '(5) ADA — assistente multi-modal com voz (Whisper/TTS) e painel admin, desenvolvido no Hackathon '
            '2025 (Senac/SC), deploy pausado por custos AWS; '
            '(6) WathsBotApp — assistente RAG para WhatsApp com Redis e Playwright, código no GitHub.'
        )

    if any(w in msg for w in ['skill', 'tecnologia', 'stack', 'linguagem', 'python', 'django']):
        return (
            'Stack principal de Renato: Python, Django, Django REST Framework, LangChain, OpenAI API, RAG, '
            'PostgreSQL, AWS (EC2/S3), Git/GitHub, Tailwind CSS. Também domina Arduino, ESP32 e MQTT '
            'para projetos IoT.'
        )

    if any(w in msg for w in ['formação', 'formacao', 'estudo', 'faculdade', 'curso', 'certificação', 'ifsc']):
        return (
            'Formação: Especialização em Computação Científica para a Indústria (IFSC – em andamento), '
            'Tecnólogo em Sistemas para Internet (Estácio de Sá – concluído), Técnico em Eletrônica (SENAI/2007). '
            'Certificações: PycodeBR Python Master (100h+, 450+ aulas), NR10, NR35.'
        )

    if any(w in msg for w in ['contato', 'email', 'telefone', 'whatsapp', 'linkedin', 'github']):
        return (
            'Contato com Renato: Email: renatoteodoro2@gmail.com | Telefone/WhatsApp: (48) 99640-4676 | '
            'Localização: Palhoça/SC – Brasil. Para mais detalhes, use o formulário de contato na seção Contato.'
        )

    if any(w in msg for w in ['quem', 'sobre', 'renato', 'perfil', 'apresentação']):
        return (
            'Renato Teodoro é um profissional com 25+ anos de experiência em eletrônica, telecomunicações e '
            'segurança eletrônica, em transição para desenvolvimento de software e IA. Combina sólido background '
            'técnico em hardware com habilidades crescentes em Python, Django, APIs e Inteligência Artificial.'
        )

    if any(w in msg for w in ['ia', 'inteligência artificial', 'langchain', 'openai', 'rag', 'agente']):
        return (
            'Renato trabalha com IA utilizando: LangChain para orquestração de LLMs, OpenAI API (GPT-4), '
            'RAG (Retrieval-Augmented Generation) para chatbots com base de conhecimento, e Agentes de IA '
            'autônomos. Desenvolveu um chatbot completo com memória de conversação como projeto.'
        )

    return (
        'Posso responder perguntas sobre o portfólio e currículo do Renato Teodoro! '
        'Tente perguntar sobre: experiências profissionais, projetos de software, skills técnicas, '
        'formação acadêmica, programa Nascer/projeto AccessFive, ou como entrar em contato.'
    )
