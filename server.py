import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "books.json"
PORT = 8000

BOOKS_INITIAL = [
    {
        "num": 1,
        "title": "Onde Vivem as Monstras",
        "author": "Aoko Matsuda",
        "genre": "Conto",
        "titleEn": "Where the Wild Ladies Are",
        "desc": "Coletânea de contos em que histórias do folclore japonês são recontadas sob uma perspectiva feminista. Mortos convivem com vivos, e o humor e o olhar feminino se entrecruzam."
    },
    {
        "num": 2,
        "title": "Os Esquecidos de Domingo",
        "author": "Valérie Perrin",
        "genre": "Romance",
        "titleEn": "Forgotten on Sunday",
        "desc": "Justine trabalha num lar de idosos numa pequena aldeia francesa, onde cria um laço profundo com Hélène, centenária cujo sonho sempre foi aprender a ler. Enquanto as conversas se multiplicam, ela começa a questionar a morte dos pais, e surgem telefonemas misteriosos."
    },
    {
        "num": 3,
        "title": "Água Fresca para as Flores",
        "author": "Valérie Perrin",
        "genre": "Romance",
        "titleEn": "Fresh Water for Flowers",
        "desc": "Violette Toussaint é zeladora de um cemitério onde sua casa funciona como abrigo diante da perda. Com quase cinquenta anos, carrega uma infância conturbada e um marido desaparecido. Tudo muda com a chegada de um homem misterioso."
    },
    {
        "num": 4,
        "title": "As Quatro Vidas de Daiyu",
        "author": "Jenny Tinghui Zhang",
        "genre": "Ficção literária",
        "titleEn": "Four Treasures of the Sky",
        "desc": "China, 1882. Daiyu é sequestrada e contrabandeada para os Estados Unidos, onde enfrenta a violência contra imigrantes chineses. Romance arrebatador sobre amor, preconceito e sobrevivência."
    },
    {
        "num": 5,
        "title": "A Paciente Silenciosa",
        "author": "Alex Michaelides",
        "genre": "Thriller / Suspense",
        "titleEn": "The Silent Patient",
        "desc": "Após matar o marido com cinco tiros, uma pintora famosa se recusa a dizer uma palavra. O psicoterapeuta Theo Faber fica obcecado em fazê-la falar. Best-seller com final eletrizante que faz o leitor questionar tudo que acabou de ler."
    },
    {
        "num": 6,
        "title": "A Morte de Vivek Oji",
        "author": "Akwaeke Emezi",
        "genre": "Ficção literária",
        "titleEn": "Death of Vivek Oji",
        "desc": "Narrativa fluida com idas e vindas temporais e múltiplas perspectivas, acompanhando personagens que orbitam ao redor de Vivek, cuja morte é anunciada no título. Obra atravessada por questões de gênero e identidade."
    },
    {
        "num": 7,
        "title": "Hábitos Atômicos",
        "author": "James Clear",
        "genre": "Desenvolvimento pessoal",
        "titleEn": "Atomic Habits",
        "desc": "Manual prático sobre como pequenas mudanças de comportamento geram resultados extraordinários. Explica como construir bons hábitos e eliminar os ruins usando a ciência do comportamento humano."
    },
    {
        "num": 8,
        "title": "Deu Zebra! Descobrindo a Superdotação",
        "author": "Sophie Prignon e Thais Mesquita",
        "genre": "Não ficção",
        "titleEn": "Deu Zebra Superdotacao",
        "desc": "Com linguagem descomplicada, traz conhecimento científico sobre a superdotação com depoimentos de pessoas identificadas tardiamente. Mostra que ser neuroatípico não é ser gênio nem problemático."
    },
    {
        "num": 9,
        "title": "Bem-Vindos à Livraria Hyunam-Dong",
        "author": "Hwang Bo-Reum",
        "genre": "Ficção literária",
        "titleEn": "Welcome to the Hyunam-dong Bookshop",
        "desc": "Yeongju decide deixar tudo para trás e abrir uma livraria — seu sonho desde a infância. A livraria se transforma num espaço onde almas feridas descansam e descobrem o que realmente importa. Fenômeno coreano."
    },
    {
        "num": 10,
        "title": "Grande Sertão: Veredas",
        "author": "João Guimarães Rosa",
        "genre": "Clássico brasileiro",
        "titleEn": "The Devil to Pay in the Backlands",
        "desc": "O maior romance da literatura brasileira. O ex-jagunço Riobaldo narra sua vida no sertão mineiro, seus combates, amizades e o amor ambíguo por Diadorim. Uma obra densa que questiona o bem, o mal e a existência do diabo."
    },
    {
        "num": 11,
        "title": "Talvez Você Deva Conversar com Alguém",
        "author": "Lori Gottlieb",
        "genre": "Autoconhecimento",
        "titleEn": "Maybe You Should Talk to Someone",
        "desc": "A terapeuta Lori Gottlieb precisa ela mesma iniciar um processo terapêutico. Combinando histórias de quatro pacientes com sua própria experiência, oferece um relato afetuoso sobre a universalidade das angústias humanas."
    },
    {
        "num": 12,
        "title": "Cartas de um Diabo ao Seu Aprendiz",
        "author": "C. S. Lewis",
        "genre": "Ficção literária",
        "titleEn": "The Screwtape Letters",
        "desc": "Correspondência cômica e original entre um diabo experiente e seu sobrinho aprendiz. Os papéis se invertem: Deus é chamado de Inimigo. Clássico da literatura cristã publicado em 1942."
    },
    {
        "num": 13,
        "title": "A Vila dos Tecidos",
        "author": "Anne Jacobs",
        "genre": "Ficção histórica",
        "titleEn": "The Tuchvilla",
        "desc": "Augsburgo, 1913. Após uma infância difícil num orfanato, a jovem Marie consegue emprego na mansão da Vila dos Tecidos, o conglomerado têxtil mais proeminente da Alemanha. Uma mansão, uma família poderosa e um segredo obscuro."
    },
    {
        "num": 14,
        "title": "Castelo Interior (ou Moradas)",
        "author": "Santa Teresa de Ávila",
        "genre": "Espiritualidade",
        "titleEn": "The Interior Castle Teresa Avila",
        "desc": "Clássico da espiritualidade cristã escrito em 1577. Teresa descreve a alma como um castelo de diamante com sete moradas, cada uma representando um estágio rumo à união com Deus. Ensinamentos para pessoas de todas as fés."
    }
]


def load_books():
    if not DATA_FILE.exists():
        save_books(BOOKS_INITIAL)
        return [dict(book) for book in BOOKS_INITIAL]
    try:
        with DATA_FILE.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list):
            raise ValueError("books.json must contain an array")
        return data
    except Exception:
        return [dict(book) for book in BOOKS_INITIAL]


def save_books(data):
    with DATA_FILE.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_GET(self):
        if self.path == "/api/books":
            books = load_books()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(books, ensure_ascii=False).encode("utf-8"))
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/books":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            try:
                payload = json.loads(body)
                title = payload.get("title", "").strip()
                author = payload.get("author", "").strip()
                genre = payload.get("genre", "").strip()
                desc = payload.get("desc", "").strip()
                cover_url = payload.get("coverUrl") or None
                if not (title and author and genre and desc):
                    raise ValueError("Campos obrigatórios ausentes")
                books = load_books()
                next_num = max((item.get("num", 0) for item in books), default=0) + 1
                book = {
                    "num": next_num,
                    "title": title,
                    "author": author,
                    "genre": genre,
                    "desc": desc,
                    "titleEn": payload.get("titleEn", ""),
                    "coverUrl": cover_url,
                    "isNew": True,
                }
                books.append(book)
                save_books(books)
                self.send_response(201)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(book, ensure_ascii=False).encode("utf-8"))
            except Exception as exc:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(exc)}, ensure_ascii=False).encode("utf-8"))
            return
        return super().do_POST()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()


if __name__ == "__main__":
    os.chdir(ROOT)
    server = HTTPServer(("", PORT), Handler)
    print(f"Servidor iniciado em http://localhost:{PORT}")
    print("Use Ctrl+C para parar.")
    server.serve_forever()
