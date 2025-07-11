from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
from schemas import UserCreate
import crud, send_email, gemini
from schemas import NewsletterCreate
from schemas import NewsletterCreate

app = FastAPI(
    title="DystopianNews Newsletter API",
    description="API para cadastro de e-mails e envio automático de newsletters geradas por IA.",
    version="1.0.0"
)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/subscribe", summary="Inscrever usuário", description="Adiciona um novo e-mail à lista de assinantes.")
def subscribe(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Cadastrar usuário
    db_user = crud.create_user(db, user)

    # 2. Gerar conteúdo da newsletter (mock ou Gemini)
    content = gemini.generate_newsletter_content()
    newsletter_data = NewsletterCreate(**content)
    
    # 3. Criar newsletter no banco (só se ainda não foi enviada hoje, opcional)
    crud.create_newsletter(db, newsletter_data)
    
    # 4. Enviar só para o novo inscrito
    email_sent = send_email.send_email(
        to=db_user.email,
        subject=content["title"],
        content=content["content"]
    )

    if not email_sent:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Usuário inscrito, mas houve erro ao enviar e-mail."}
        )

    return {"message": f"{db_user.email} inscrito e newsletter enviada com sucesso."}

@app.post("/send-newsletter", summary="Enviar newsletter", description="Envia a newsletter gerada para todos os assinantes.")
def send_newsletter(db: Session = Depends(get_db)):
    content = gemini.generate_newsletter_content()
    newsletter_data = NewsletterCreate(**content)  # transforma o dict num Pydantic
    newsletter = crud.create_newsletter(db, newsletter_data)

    users = crud.get_users(db)
    for user in users:
        send_email.send_email(user.email, content["title"], content["content"])

    return {"message": f"Newsletter enviada para {len(users)} usuários"}