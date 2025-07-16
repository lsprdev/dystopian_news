# Trabalho Final – Fundamentos de DevOps
**Aluno:** Gabriel Lopes Pereira  

## 1. Introdução
O projeto **Dystopian News** consiste em uma aplicação web _full‑stack_ que publica notícias geradas por inteligência artificial.  
O objetivo deste trabalho é demonstrar a aplicação prática dos fundamentos de **DevOps**, cobrindo todo o ciclo de vida: **Infraestrutura como Código**, **CI/CD**, **GitOps** e **observabilidade**.  
As principais tecnologias empregadas foram: **Terraform**, **Docker**, **Kubernetes (DOKS)**, **Argo CD**, **GitHub Actions**, **FastAPI**, **Next.js** e **PostgreSQL**.

## 2. Escolha do Ambiente
| Critério              | Decisão                                       | Justificativa                                                         |
| --------------------- | --------------------------------------------- | --------------------------------------------------------------------- |
| Tipo de ambiente      | **Cloud – DigitalOcean** + contêineres Docker | Provisionamento rápido, custo previsível e integração nativa com DOKS |
| Modelo de implantação | **Cluster Kubernetes gerenciado** (DOKS)      | Alta disponibilidade e escalabilidade sem gerenciar plano de controle |
| Banco de dados        | **PostgreSQL gerenciado** (DigitalOcean DB)   | Backups automáticos e _fail‑over_                                     |

**Descrição das instâncias criadas**

* Cluster DOKS: 3 nós `s-2vcpu-4gb`, versão `1.33.1‑do.1`, região `nyc1`.  
* Banco PostgreSQL: 1 nó primário `db-s-1vcpu-1gb` com backups diários.  

## 3. Provisionamento
* **Ferramentas**: `Terraform` (arquivos em `infra/*.tf`)  
* **Fluxo**:
  1. Criação do cluster Kubernetes e banco PostgreSQL.  
  2. Outputs exportam o `kubeconfig` e a `DATABASE_URL` como _outputs sensíveis_.  
* **Desafios & Soluções**  
  - **Limitação de versionamento do DOKS**  ➜ Pinagem da versão (`1.33.1-do.1`).  
  - **Rotação de token da DigitalOcean**  ➜ Armazenado no **Terraform Cloud** como variável sensível.

## 4. Cluster Kubernetes
* **Instalação**: DOKS provisionado via API pelo Terraform.  
* **Configuração dos nós**: 3 workers `s-2vcpu-4gb` (4 GB RAM / 2 vCPU) – _node pools_ escaláveis.  
* **Testes**  
  ```bash
  kubectl get nodes
  kubectl run hello --image=nginx -n default --port 80
  kubectl port-forward pod/hello 8080:80
  ```
  Retorno 200 confirma funcionamento da malha de rede e _ingress_.

## 5. GitOps com ArgoCD
* **Instalação**: Helm chart `argo/argo-cd`, namespace `argocd`.  
* **Configuração do repositório**: Path `infra/k8s`, branch `main`, modo _Auto‑Sync_.  
* **Deploy da aplicação**: ArgoCD aplica `Deployment`, `Service` e `Ingress` para backend e frontend.  
* **Screenshots**  
```
![Visão geral de aplicações](screenshots/argocd-apps.png)
![Sync bem‑sucedido](screenshots/argocd-sync.png)
```

## 6. Aplicação
| Componente | Tecnologia           | Container / Porta               | Descrição                                              |
| ---------- | -------------------- | ------------------------------- | ------------------------------------------------------ |
| Backend    | **FastAPI** (Python) | `dystopian-news-backend` :8000  | API REST + endpoints "/subscribe" & "/send_newsletter" |
| Frontend   | **Next.js** (TS)     | `dystopian-news-frontend` :3000 | Interface de notícias                                  |
| Banco      | **PostgreSQL 15**    | Serviço gerenciado              | Persistência de usuários e newsletters                 |

**Acesso**  
```text
https://dn.lsx.li      ← Frontend
https://eipiai.lsx.li  ← Backend
```

## 7. Conclusão
**Lições aprendidas**
* GitOps reduz o esforço manual de deploys e oferece _rollback_ instantâneo.  
* Terraform + DOKS simplificam muito a gestão de infraestrutura.

**Dificuldades**
* Conciliação de tags de imagem entre GitHub Actions e ArgoCD.  
* Ajustar certificados TLS para o Ingress.

**O que faria diferente**
* Adicionar _monitoramento_ com Prometheus + Grafana.  
* Implementar _pipelines_ de teste (pytest, Cypress) antes do build.

## 8. Link para Repositório
<https://github.com/lsprdev/dystopian_news>
