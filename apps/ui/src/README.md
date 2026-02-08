# Sistema de Atendimento via WhatsApp

Sistema multi-tenant de atendimento ao cliente via WhatsApp com gestão de usuários, permissões e métricas.

## 🚀 Funcionalidades

### Autenticação e Autorização

- ✅ Sistema multi-tenant (múltiplas empresas)
- ✅ 3 tipos de usuários com permissões distintas
- ✅ Login seguro com validação de sessão
- ✅ Sistema granular de permissões baseado em roles
- ✅ Isolamento completo de dados por empresa

### Gestão de Conversas

- ✅ Lista de conversas em tempo real
- ✅ Chat completo com mensagens
- ✅ Atribuição de conversas a atendentes
- ✅ Filtros por status (ativas, pendentes, resolvidas)
- ✅ Indicadores de mensagens não lidas
- ✅ Busca de conversas

### Gestão de Atendentes

- ✅ Visualização de atendentes
- ✅ Status online/away/offline
- ✅ Métricas por atendente
- ✅ Conversas ativas e totais

### Gestão de Usuários

- ✅ Criação de usuários com validação de permissões
- ✅ Administradores podem criar qualquer tipo de usuário
- ✅ Gerentes podem criar apenas atendentes
- ✅ Atendentes não podem criar usuários
- ✅ Visualização de todos os usuários da empresa

### Dashboard e Métricas

- ✅ KPIs principais (conversas, tempo de resposta, satisfação)
- ✅ Gráficos de conversas por dia
- ✅ Distribuição de status
- ✅ Performance por atendente
- ✅ Volume por horário
- ✅ Tabela detalhada de performance

## 🏗️ Arquitetura

O projeto segue os princípios do **Clean Architecture**:

```
📁 domain/              # Regras de negócio (entities, use cases, interfaces)
📁 data/                # Implementações dos repositórios
📁 infrastructure/      # Injeção de dependências
📁 presentation/        # Componentes React e hooks
```

Veja [ARCHITECTURE.md](./ARCHITECTURE.md) para detalhes completos.

## 👥 Tipos de Usuários

### 1. ADMINISTRATOR (Administrador)

- ✅ Acesso total ao sistema
- ✅ Gerencia todos os usuários
- ✅ Visualiza todas as conversas e métricas
- ✅ Configura a empresa

### 2. MANAGER (Gerente)

- ✅ Cria e gerencia atendentes
- ✅ Visualiza todas as conversas
- ✅ Atribui conversas
- ✅ Acessa métricas da equipe

### 3. ATTENDANT (Atendente)

- ✅ Visualiza conversas atribuídas
- ✅ Responde mensagens
- ✅ Visualiza próprias métricas

Veja [AUTHENTICATION.md](./AUTHENTICATION.md) para detalhes sobre permissões.

## 🔐 Contas de Teste

### Empresa: Tech Solutions Ltda

**Administrador:**

```
Email: admin@techsolutions.com
Senha: 123456
```

**Gerente:**

```
Email: carlos@techsolutions.com
Senha: 123456
```

**Atendente:**

```
Email: joao@techsolutions.com
Senha: 123456
```

### Empresa: Comércio Digital SA

**Administrador:**

```
Email: admin@comerciodigital.com
Senha: 123456
```

## 🛠️ Tecnologias

- **React** - Interface do usuário
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização
- **Recharts** - Gráficos e visualizações
- **Lucide React** - Ícones
- **ShadCN UI** - Componentes base

## 📂 Estrutura do Projeto

```
/
├── domain/                      # Camada de Domínio
│   ├── entities/               # Modelos de negócio
│   │   ├── Company.ts
│   │   ├── User.ts
│   │   ├── Permission.ts
│   │   ├── Conversation.ts
│   │   ├── Message.ts
│   │   ├── Attendant.ts
│   │   └── Metrics.ts
│   ├── repositories/           # Interfaces dos repositórios
│   │   ├── ICompanyRepository.ts
│   │   ├── IUserRepository.ts
│   │   ├── IAuthRepository.ts
│   │   ├── IConversationRepository.ts
│   │   └── IMetricsRepository.ts
│   └── use-cases/             # Casos de uso
│       ├── auth/
│       │   ├── Login.ts
│       │   ├── Logout.ts
│       │   └── ValidateSession.ts
│       ├── user/
│       │   ├── CreateUser.ts
│       │   ├── GetUsersByCompany.ts
│       │   └── CheckPermission.ts
│       └── ...
│
├── data/                       # Implementações
│   └── repositories/
│       ├── CompanyRepository.ts
│       ├── UserRepository.ts
│       ├── AuthRepository.ts
│       ├── ConversationRepository.ts
│       └── MetricsRepository.ts
│
├── infrastructure/             # Infraestrutura
│   └── di/
│       └── container.ts       # Dependency Injection
│
├── presentation/              # Camada de Apresentação
│   ├── components/
│   │   ├── Login.tsx
│   │   ├── Sidebar.tsx
│   │   ├── ConversationList.tsx
│   │   ├── ChatArea.tsx
│   │   ├── AttendantPanel.tsx
│   │   ├── Dashboard.tsx
│   │   ├── UserManagement.tsx
│   │   ├── ProtectedRoute.tsx
│   │   └── RoleBadge.tsx
│   ├── contexts/
│   │   └── AuthContext.tsx
│   └── hooks/
│       ├── useAuth.ts
│       ├── useConversations.ts
│       ├── useConversationMessages.ts
│       ├── useAttendants.ts
│       ├── useMetrics.ts
│       └── useUsers.ts
│
└── App.tsx                    # Componente principal
```

## 🔒 Segurança

### Implementado

- ✅ Autenticação baseada em token
- ✅ Validação de sessão
- ✅ Isolamento de dados por empresa
- ✅ Sistema de permissões granular
- ✅ Validação em use cases

### Para Produção

- [ ] Hash de senhas (bcrypt/argon2)
- [ ] Refresh tokens
- [ ] Rate limiting
- [ ] 2FA (autenticação de dois fatores)
- [ ] Logs de auditoria
- [ ] HTTPS obrigatório

## 🎨 Design

- **Minimalista**: Interface limpa e focada
- **Intuitivo**: Navegação clara e direta
- **Responsivo**: Funciona em diferentes tamanhos de tela
- **Acessível**: Uso de cores e contrastes adequados

## 📊 Métricas e KPIs

O dashboard apresenta:

- Total de conversas (com tendência)
- Tempo médio de resposta
- Taxa de satisfação
- Atendentes ativos
- Conversas por dia (gráfico)
- Status das conversas (pizza)
- Performance por atendente (barras)
- Volume por horário
- Tabela detalhada de performance

## 🔄 Fluxo de Dados

```
User Action
    ↓
Component (UI)
    ↓
Custom Hook
    ↓
Use Case (Business Logic)
    ↓
Repository Interface
    ↓
Repository Implementation
    ↓
Data Source (Mock/API)
```

## 🧪 Testing

A arquitetura facilita testes:

```typescript
// Testar use case isoladamente
const mockRepository = {
  authenticate: jest.fn().mockResolvedValue(mockSession)
};
const loginUseCase = new Login(mockRepository);

// Testar componente com hook mockado
const mockUseAuth = () => ({ session: mockSession, ... });
```

## 📝 Como Usar

### Login

1. Acesse o sistema
2. Digite email e senha
3. Sistema valida e cria sessão
4. Redirecionado para dashboard

### Criar Usuário

1. Menu lateral > Usuários
2. Clique em "Novo Usuário"
3. Preencha dados
4. Selecione tipo (baseado em suas permissões)
5. Clique em "Criar Usuário"

### Gerenciar Conversas

1. Menu lateral > Conversas
2. Selecione uma conversa
3. Visualize histórico
4. Atribua a atendente (se tiver permissão)
5. Responda mensagens

### Visualizar Métricas

1. Menu lateral > Dashboard
2. Visualize KPIs
3. Analise gráficos
4. Exporte relatórios (futuro)

## 🚀 Próximos Passos

### Curto Prazo

- [ ] Implementar filtros de conversas
- [ ] Adicionar busca em tempo real
- [ ] Notificações de novas mensagens
- [ ] Edição de usuários
- [ ] Desativação de usuários

### Médio Prazo

- [ ] Integração real com API do WhatsApp
- [ ] WebSocket para mensagens em tempo real
- [ ] Upload de arquivos e mídia
- [ ] Templates de mensagens
- [ ] Respostas rápidas

### Longo Prazo

- [ ] Chatbot com IA
- [ ] Análise de sentimentos
- [ ] Relatórios avançados
- [ ] Integrações com CRM
- [ ] API pública

## 📚 Documentação Adicional

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Detalhes da arquitetura Clean Architecture
- [AUTHENTICATION.md](./AUTHENTICATION.md) - Sistema de autenticação e permissões
- [domain/README.md](./domain/README.md) - Camada de domínio
- [presentation/README.md](./presentation/README.md) - Camada de apresentação

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é um protótipo para demonstração.

## 👨‍💻 Desenvolvido com

- ❤️ Paixão por código limpo
- 🏗️ Clean Architecture
- 🎨 Design minimalista
- 🔐 Segurança em mente
- 📱 Pensando mobile-first

---

**Nota**: Este é um sistema de demonstração com dados mock. Para produção, implemente as camadas de segurança adicionais mencionadas.
