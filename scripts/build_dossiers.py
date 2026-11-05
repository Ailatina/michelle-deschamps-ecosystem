"""Build the ES and EN commercial PDFs in the repository root.

Run with Python 3, reportlab, pypdf and DejaVu Sans installed.
The public files keep their v2 URLs while the document shows its current revision.
"""
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape
from base64 import a85encode
from zlib import compress

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, NameObject, StreamObject, TextStringObject
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

OUTPUT = Path(__file__).resolve().parents[1]
PORTFOLIO = 'https://ailatina.github.io/michelle-deschamps-ecosystem/'
AINAVY, INK, GREY, PURPLE, LIGHT = [HexColor(x) for x in ('#080F25','#0F1020','#515D70','#6221C2','#F7F7F2')]
for name, file in [('BrandSans','DejaVuSans.ttf'),('BrandBold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))

def style(key,font,size,leading,color,after,before=0):
    return ParagraphStyle(key,fontName=font,fontSize=size,leading=leading,textColor=color,
                          spaceAfter=after,spaceBefore=before,allowWidows=0,allowOrphans=0)

styles={
    'k':style('section','BrandBold',9,13,PURPLE,16),
    'h':style('cover and feature','BrandBold',37,42,AINAVY,22),
    'h2':style('heading','BrandBold',28,33,AINAVY,17),
    'h3':style('topic','BrandBold',14,18,INK,5,10),
    'lead':style('intro','BrandSans',16,23,GREY,20),
    'body':style('body','BrandSans',12,18,INK,12),
    'small':style('note','BrandSans',10.2,15.3,GREY,13),
    'link':style('action','BrandBold',11,16.5,PURPLE,12)
}

DATA={
'es':{
    'footer':'Presentación comercial · versión 2.1 · 5 de noviembre de 2026',
    'cover':'IA con propósito.<br/>Estrategia que se<br/>puede ejecutar.',
    'intro':'AiLatina ayuda a equipos de servicios a ordenar su seguimiento comercial y adoptar IA con criterio humano.',
    'bio':'Soy Michelle R. Deschamps, fundadora de AiLatina. En la hotelería aprendí a escuchar lo que necesitaba cada huésped. En ventas vi cómo una conversación prometedora se pierde cuando nadie se encarga del próximo paso. Hoy diseño software y enseño a los equipos a resolver ese problema en español e inglés.',
    'bio_link':'Conoce mi trayectoria y mis proyectos',
    'offer':'EL PUNTO DE ENTRADA', 'audit':'Auditoría de<br/>seguimiento comercial',
    'audit_intro':'US$497 · pago único por adelantado. Un negocio, un proceso de seguimiento y un idioma, español o inglés.',
    'deliverables':[
        ('Qué revisamos','Hasta 20 consultas comerciales anonimizadas de los últimos 30 días. Trabajamos contigo en un diagnóstico de 60 minutos y una sesión de entrega de 30 minutos, según disponibilidad.'),
        ('Qué te llevas','Mapa del proceso actual y el propuesto, hasta tres brechas respaldadas por evidencia, tres mensajes reutilizables, un procedimiento con responsable y un plan de acción de 30 días.'),
        ('Cuándo se entrega','Informe dentro de 48 horas hábiles tras el diagnóstico y la recepción de la evidencia completa. Incluye una ronda consolidada de correcciones en cinco días hábiles y una revisión asíncrona al día siete de hasta 15 minutos.')
    ],
    'scope':'La implementación y las licencias se cotizan aparte. Consulta el alcance, el crédito aplicable a los servicios elegibles y la política de cancelación en la página de la auditoría.',
    'audit_link':'Ver alcance, condiciones y reserva',
    'brands_heading':'Dónde encaja cada proyecto',
    'brands':[
        ('Michelle Deschamps','El portafolio reúne mi trayectoria, mis libros, mis aplicaciones y los casos que puedo documentar.'),
        ('AiLatina y AiLatina Agents','AiLatina ofrece consultoría y educación en vivo. AiLatina Agents se especializa en recuperar consultas y citas con seguimiento asistido por IA y revisión humana.'),
        ('The Audio Healer','Curaduría musical y experiencias de escucha para eventos corporativos, hoteles y retiros.'),
        ('Aluma Conscious Stays','Diseño y curaduría de interiores y espacios conscientes de hospitalidad. Casa Sur sigue en desarrollo.'),
        ('Future-Proof Collective','Red de especialistas que colaboran según el alcance de cada proyecto.'),
        ('One Moment Design','Identidad en desarrollo dentro del ecosistema.')
    ],
    'portfolio_link':'Explorar el software y su estado',
    'method_label':'METODOLOGÍA Y CONTACTO','method_title':'Cómo trabajamos',
    'framework_title':'The Future Proof Method',
    'framework':'Michelle Deschamps creó el método y el libro del mismo nombre. En AiLatina, lo aplicamos para definir quién responde por un proceso, qué puede hacer la IA y cuándo interviene una persona.',
    'method_link':'Leer sobre el método de Michelle',
    'source_title':'Aprendizajes de BMS',
    'source':'Nuestro proceso de diagnóstico, oferta y entrega incorpora aprendizajes de BMS de Vilma Núñez y Grupo Convierte Más. Para mostrar la trayectoria, el trabajo y las ofertas de Michelle en el portafolio, adaptamos ejercicios de activos de marca personal que imparte Maru Matos dentro de BMS en Journi.',
    'live_title':'Para tu equipo o tu evento',
    'live':'En un taller en vivo trabajamos un proceso real y salimos con un mapa, un responsable y un criterio de prueba. Para un evento corporativo u hotelero, diseñamos la experiencia, el recorrido del público y la música a partir de un brief.',
    'lab_link':'Consultar por un taller','event_link':'Preparar un evento',
    'case_link':'Leer el caso preparado de CACODIA','radar_link':'Visitar Radar RD',
    'contact_title':'Contacto de proyecto','apply_link':'Iniciar una consulta con AiLatina'
},
'en':{
    'footer':'Business introduction · version 2.1 · November 5, 2026',
    'cover':'Purposeful AI.<br/>Strategy you can<br/>put into practice.',
    'intro':'AiLatina helps service teams organize commercial follow-up and adopt AI with human judgment.',
    'bio':'I’m Michelle R. Deschamps, founder of AiLatina. Hospitality taught me to listen for what a guest needed. In sales I saw promising conversations get lost when nobody owned the next step. Today I design software and teach teams how to solve that problem in English and Spanish.',
    'bio_link':'Explore my background and projects',
    'offer':'WHERE TO BEGIN','audit':'Lead Follow-up<br/>Audit',
    'audit_intro':'US$497 · one-time payment before work starts. One business, one follow-up process and one language, English or Spanish.',
    'deliverables':[
        ('What we review','Up to 20 de-identified sales inquiries from the last 30 days. We work with you in a 60-minute diagnostic and a 30-minute handoff, scheduled subject to availability.'),
        ('What you receive','A map of the current and proposed process, up to three gaps backed by evidence, three reusable messages, a procedure with a named owner and a 30-day action plan.'),
        ('When you receive it','A written report within 48 business hours after the diagnostic and receipt of complete evidence. Includes one consolidated round of corrections within five business days and an asynchronous day-seven review of up to 15 minutes.')
    ],
    'scope':'Implementation and software licenses are priced separately. The audit page sets out the scope, credit toward eligible services and cancellation terms.',
    'audit_link':'View the scope, terms and booking',
    'brands_heading':'Where each project fits',
    'brands':[
        ('Michelle Deschamps','My portfolio brings together my background, books, applications and cases I can document.'),
        ('AiLatina and AiLatina Agents','AiLatina provides consulting and live education. AiLatina Agents focuses on recovering leads and appointments through AI-assisted follow-up and human review.'),
        ('The Audio Healer','Music curation and listening experiences for corporate events, hotels and retreats.'),
        ('Aluma Conscious Stays','Interior design and curation for thoughtful hospitality spaces. Casa Sur is in development.'),
        ('Future-Proof Collective','A network of specialists who collaborate according to the needs of each project.'),
        ('One Moment Design','A brand identity in development within the ecosystem.')
    ],
    'portfolio_link':'Explore the software and its release status',
    'method_label':'METHODOLOGY AND CONTACT','method_title':'How we work',
    'framework_title':'The Future Proof Method',
    'framework':'Michelle Deschamps created the method and the book of the same name. At AiLatina, we use it to define who owns a process, what AI can do and when a person takes over.',
    'method_link':'Read about Michelle’s method',
    'source_title':'Lessons from BMS',
    'source':'Our diagnostic, offer design and delivery process incorporates learning from BMS by Vilma Núñez and Grupo Convierte Más. To present Michelle’s background, work and offers in the portfolio, we adapted the personal-brand asset exercises taught by Maru Matos within BMS on Journi.',
    'live_title':'For your team or event',
    'live':'In a live workshop we use a real workflow to create a map, name an owner and set a test criterion. For a corporate or hotel event, we use your brief to design the guest journey, the atmosphere and the music.',
    'lab_link':'Ask about a workshop','event_link':'Plan an event',
    'case_link':'Read the CACODIA proposal case','radar_link':'Visit Radar RD',
    'contact_title':'Project contact','apply_link':'Start an inquiry with AiLatina'
}}

def link(label,url):
    return f'<link href="{escape(url)}" color="#6221C2"><u>{escape(label)}</u></link>'

def write_ascii_pdf(path,lang):
    reader=PdfReader(path)
    writer=PdfWriter()
    writer.clone_document_from_reader(reader)
    writer._root_object[NameObject('/Lang')]=TextStringObject(lang)
    for obj in writer._objects:
        if isinstance(obj,StreamObject):
            obj._data=a85encode(compress(obj.get_data(),9))+b'~>'
            obj[NameObject('/Filter')]=ArrayObject([NameObject('/ASCII85Decode'), NameObject('/FlateDecode')])
            obj.pop('/DecodeParms',None)
    buf=BytesIO()
    writer.write(buf)
    data=buf.getvalue()
    nl=data.index(b'\n')+1
    second=data.index(b'\n',nl)
    data=data[:nl]+bytes(b if b<128 else 65 for b in data[nl:second])+data[second:]
    data.decode('ascii')
    path.write_bytes(data)

def build(lang):
    c=DATA[lang];out=OUTPUT/f'ailatina-dossier-{lang}-v2.pdf'
    portrait_url=f'{PORTFOLIO}?brand=michelle-deschamps&lang={lang}'
    case_url='https://ailatina.ai/blog/caso-cacodia-diseno-institucional'+('-en' if lang=='en' else '')
    story=[]
    def add(value,kind='body'):
        story.append(Paragraph(value,styles[kind]))
    def gap(points):story.append(Spacer(1,points))
    def footer(canvas,doc):
        width,height=A4
        canvas.setFillColor(LIGHT);canvas.rect(0,0,width,height,stroke=0,fill=1)
        canvas.setFillColor(AINAVY);canvas.setFont('BrandBold',11);canvas.drawString(52,height-37,'AiLatina')
        canvas.setFont('BrandSans',8);canvas.setFillColor(GREY);canvas.drawRightString(width-52,height-37,lang.upper()+' / V2.1')
        canvas.setStrokeColor(HexColor('#DBDEE5'));canvas.line(52,48,width-52,48)
        canvas.drawString(52,32,c['footer']);canvas.drawRightString(width-52,32,f'{doc.page} / 4')
    doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=52,rightMargin=52,topMargin=70,bottomMargin=64,
                          pageCompression=1,title=f'AiLatina Dossier {lang.upper()} v2.1',author='Michelle Deschamps')
    add('MICHELLE DESCHAMPS · AILATINA','k');gap(41)
    add(c['cover'],'h');add(c['intro'],'lead');add(c['bio']);gap(21)
    add(link(c['bio_link'],portrait_url+'#historia'),'link');add(link('ailatina.ai','https://ailatina.ai'),'link')
    story.append(PageBreak())
    add(c['offer'],'k');add(c['audit'],'h');add(c['audit_intro'],'lead')
    for title,body in c['deliverables']:add(title,'h3');add(body)
    gap(4);add(c['scope'],'small');add(link(c['audit_link'],'https://ailatina.ai/auditoria'),'link')
    story.append(PageBreak())
    add('MICHELLE DESCHAMPS','k');add(c['brands_heading'],'h2')
    for title,body in c['brands']:add(title,'h3');add(body)
    gap(6);add(link(c['portfolio_link'],portrait_url+'#software'),'link')
    story.append(PageBreak())
    add(c['method_label'],'k');add(c['method_title'],'h2')
    add(c['framework_title'],'h3');add(c['framework']);add(link(c['method_link'],'https://ailatina.ai/futureproofmethod'),'link')
    add(c['source_title'],'h3');add(c['source'])
    add(c['live_title'],'h3');add(c['live'])
    add(link(c['lab_link'],portrait_url+'#talleres')+'  ·  '+link(c['event_link'],portrait_url+'#eventos'),'link')
    add(link(c['case_link'],case_url)+'  ·  '+link(c['radar_link'],'https://radar-rd.ailatina.chatgpt.site/'),'link')
    add(c['contact_title'],'h3')
    add(link(c['apply_link'],'https://ailatina.ai/apply')+'  ·  '+link('theailatina@gmail.com','mailto:theailatina@gmail.com'),'link')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    write_ascii_pdf(out,lang)
    reader=PdfReader(out)
    assert len(reader.pages)==4,(out,len(reader.pages))
    assert reader.metadata.title.endswith('v2.1')
    assert reader.trailer['/Root']['/Lang']==lang
    texts=[" ".join(p.extract_text().split()) for p in reader.pages]
    assert '497' in texts[1] and 'Maru Matos' in texts[3] and 'Vilma Núñez' in texts[3]
    assert 'Grupo Convierte Más' in texts[3] and 'Journi' in texts[3] and 'The Future Proof Method' in texts[3]
    urls=[a.get_object()['/A']['/URI'] for p in reader.pages for a in p.get('/Annots',[])]
    for expected in [case_url,'https://ailatina.ai/auditoria','https://ailatina.ai/apply','https://radar-rd.ailatina.chatgpt.site/',portrait_url+'#talleres',portrait_url+'#eventos']:
        assert expected in urls,(lang,expected,urls)
    print(lang,len(out.read_bytes()),'bytes, 4 pages,',len(urls),'verified links')
if __name__ == '__main__':
    for lang in ('es','en'):
        build(lang)
