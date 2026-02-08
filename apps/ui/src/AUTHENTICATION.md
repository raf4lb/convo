# Sistema de Autenticação e Permissões

## Visão Geral

O sistema implementa um modelo **multi-tenant** com autenticação baseada em roles (papéis) e um sistema granular de permissões. Cada empresa tem seus próprios dados, usuários e configurações isoladas.

## Arquitetura Multi-Tenant

### Isolamento de Dados

Cada empresa (tenant) possui:

- ✅ Seus próprios usuários (ADMINISTRATOR, MANAGER, ATTENDANT)
- ✅ Suas próprias conversas e mensagens
- ✅ Seus próprios clientes/contatos
- ✅ Suas próprias métricas e relatórios
- ✅ Configurações independentes

### Estrutura de Empresa (Company)

```typescript
interface Company {
  id: string;
  name: string;
  email: string;
  phone: string;
  whatsappApiKey?: string;
  createdAt: Date;
  isActive: boolean;
}
```

## Tipos de Usuários (Roles)

### 1. ADMINISTRATOR (Administrador)

**Acesso Total** - Controle completo da empresa

#### Permissões:

- ✅ Criar/editar/deletar ADMINISTRATORS
- ✅ Criar/editar/deletar MANAGERS
- ✅ Criar/editar/deletar ATTENDANTS
- ✅ Visualizar todos os usuários
- ✅ Visualizar todas as conversas
- ✅ Atribuir conversas a qualquer atendente
- ✅ Editar configurações da empresa
- ✅ Visualizar todas as métricas e relatórios
- ✅ Acesso ao dashboard completo

#### Casos de Uso:

- Dono da empresa
- Gerente geral com controle total
- Responsável pela conta

### 2. MANAGER (Gerente)

**Gerenciamento Operacional** - Supervisiona atendentes

#### Permissões:

- ✅ Criar/editar/deletar ATTENDANTS
- ✅ Visualizar todos os usuários
- ✅ Visualizar todas as conversas
- ✅ Atribuir conversas a atendentes
- ✅ Visualizar informações da empresa
- ✅ Visualizar todas as métricas da equipe
- ✅ Acesso ao dashboard

#### Restrições:

- ❌ Não pode criar ADMINISTRATORS
- ❌ Não pode criar MANAGERS
- ❌ Não pode editar configurações da empresa

#### Casos de Uso:

- Supervisor de equipe
- Coordenador de atendimento
- Líder de operações

### 3. ATTENDANT (Atendente)

**Atendimento** - Responde conversas

#### Permissões:

- ✅ Visualizar conversas atribuídas
- ✅ Responder mensagens
- ✅ Visualizar informações da empresa
- ✅ Visualizar próprias métricas

#### Restrições:

- ❌ Não pode criar usuários
- ❌ Não pode visualizar conversas de outros atendentes
- ❌ Não pode atribuir conversas
- ❌ Não pode visualizar métricas de outros
- ❌ Acesso limitado ao dashboard

#### Casos de Uso:

- Atendente de suporte
- Operador de chat
- Agente de relacionamento

## Sistema de Permissões

### Permissões Disponíveis

```typescript
enum Permission {
  // Gerenciamento de Usuários
  CREATE_ADMINISTRATOR,
  CREATE_MANAGER,
  CREATE_ATTENDANT,
  UPDATE_USER,
  DELETE_USER,
  VIEW_USERS,

  // Gerenciamento de Conversas
  VIEW_CONVERSATIONS,
  ASSIGN_CONVERSATION,
  VIEW_ALL_CONVERSATIONS,

  // Gerenciamento da Empresa
  UPDATE_COMPANY,
  VIEW_COMPANY,

  // Métricas
  VIEW_DASHBOARD,
  VIEW_ALL_METRICS,
  VIEW_OWN_METRICS,
}
```

### Matriz de Permissões

| Permissão              | ADMINISTRATOR | MANAGER | ATTENDANT |
| ---------------------- | ------------- | ------- | --------- |
| CREATE_ADMINISTRATOR   | ✅            | ❌      | ❌        |
| CREATE_MANAGER         | ✅            | ❌      | ❌        |
| CREATE_ATTENDANT       | ✅            | ✅      | ❌        |
| UPDATE_USER            | ✅            | ❌      | ❌        |
| DELETE_USER            | ✅            | ❌      | ❌        |
| VIEW_USERS             | ✅            | ✅      | ❌        |
| VIEW_CONVERSATIONS     | ✅            | ✅      | ✅        |
| ASSIGN_CONVERSATION    | ✅            | ✅      | ❌        |
| VIEW_ALL_CONVERSATIONS | ✅            | ✅      | ❌        |
| UPDATE_COMPANY         | ✅            | ❌      | ❌        |
| VIEW_COMPANY           | ✅            | ✅      | ✅        |
| VIEW_DASHBOARD         | ✅            | ✅      | ❌        |
| VIEW_ALL_METRICS       | ✅            | ✅      | ❌        |
| VIEW_OWN_METRICS       | ❌            | ❌      | ✅        |

## Fluxo de Autenticação

### 1. Login

```
User submits credentials
      ↓
Login Use Case validates email/password
      ↓
AuthRepository authenticates user
      ↓
Validates user is active
      ↓
Validates company is active
      ↓
Creates session with token
      ↓
Stores token in localStorage
      ↓
Returns AuthSession
```

### 2. Session Validation

```
App loads
      ↓
Retrieves token from localStorage
      ↓
ValidateSession Use Case checks token
      ↓
Verifies token is not expired
      ↓
Returns user session with company data
```

### 3. Permission Check

```
User tries to perform action
      ↓
Component checks permission via useAuth hook
      ↓
CheckPermission Use Case validates role
      ↓
Returns true/false
      ↓
Action is allowed or denied
```

## Uso no Código

### Verificar Permissão no Componente

```typescript
import { useAuth } from '../contexts/AuthContext';
import { Permission } from '../../domain/entities/Permission';

function MyComponent() {
  const { hasPermission } = useAuth();

  const canCreateUser = hasPermission(Permission.CREATE_ATTENDANT);

  return (
    <div>
      {canCreateUser && (
        <button>Criar Atendente</button>
      )}
    </div>
  );
}
```

### Verificar Múltiplas Permissões

```typescript
const { hasAnyPermission } = useAuth();

const canManageUsers = hasAnyPermission([
  Permission.CREATE_ADMINISTRATOR,
  Permission.CREATE_MANAGER,
  Permission.CREATE_ATTENDANT,
]);
```

### Acessar Dados da Sessão

```typescript
const { session } = useAuth();

if (session) {
  console.log("User:", session.user.name);
  console.log("Company:", session.company.name);
  console.log("Role:", session.user.role);
}
```

## Use Cases de Autenticação

### Login

```typescript
const session = await loginUseCase.execute(email, password);
```

**Validações:**

- Email válido
- Senha com mínimo 6 caracteres
- Usuário existe
- Senha correta
- Usuário ativo
- Empresa ativa

### Logout

```typescript
await logoutUseCase.execute(token);
```

### Validar Sessão

```typescript
const session = await validateSessionUseCase.execute(token);
```

## Use Cases de Usuários

### Criar Usuário

```typescript
const user = await createUserUseCase.execute(
  {
    companyId: "1",
    name: "João Silva",
    email: "joao@empresa.com",
    password: "123456",
    role: UserRole.ATTENDANT,
  },
  creatorRole, // Role do usuário que está criando
);
```

**Validações:**

- Permissão para criar o tipo de usuário
- Nome com mínimo 3 caracteres
- Email válido
- Senha com mínimo 6 caracteres
- Email não está em uso

### Obter Usuários da Empresa

```typescript
const users = await getUsersByCompanyUseCase.execute(companyId, userRole);
```

**Validações:**

- Usuário tem permissão VIEW_USERS

## Segurança

### Tokens

- Gerados aleatoriamente
- Armazenados em memória (Map)
- Expiram em 24 horas
- Validados em cada requisição

### Senhas

⚠️ **Nota de Produção**: Atualmente as senhas são armazenadas em texto plano para simplicidade do mock. Em produção:

- Use bcrypt ou argon2 para hash
- Nunca retorne senhas nas respostas
- Implemente política de senhas fortes

### Isolamento de Dados

- Todos os dados são filtrados por `companyId`
- Usuários só acessam dados de sua empresa
- Validações em nível de use case

## Contas de Teste

### Empresa: Tech Solutions Ltda

**Administrador:**

- Email: `admin@techsolutions.com`
- Senha: `123456`
- Acesso: Total

**Gerente:**

- Email: `carlos@techsolutions.com`
- Senha: `123456`
- Acesso: Gerenciamento de atendentes

**Atendente:**

- Email: `joao@techsolutions.com`
- Senha: `123456`
- Acesso: Atendimento

### Empresa: Comércio Digital SA

**Administrador:**

- Email: `admin@comerciodigital.com`
- Senha: `123456`
- Acesso: Total

## Extensibilidade

### Adicionar Nova Permissão

1. Adicione ao enum `Permission`:

```typescript
enum Permission {
  // ...
  NEW_PERMISSION = "NEW_PERMISSION",
}
```

2. Adicione aos roles necessários:

```typescript
export const RolePermissions: Record<UserRole, Permission[]> = {
  [UserRole.ADMINISTRATOR]: [
    // ...
    Permission.NEW_PERMISSION,
  ],
  // ...
};
```

3. Use no componente:

```typescript
const canDoSomething = hasPermission(Permission.NEW_PERMISSION);
```

### Adicionar Novo Role

1. Adicione ao enum `UserRole`:

```typescript
enum UserRole {
  // ...
  NEW_ROLE = "NEW_ROLE",
}
```

2. Defina permissões:

```typescript
export const RolePermissions: Record<UserRole, Permission[]> = {
  // ...
  [UserRole.NEW_ROLE]: [Permission.SOME_PERMISSION],
};
```

3. Atualize use cases de criação de usuários

## Melhores Práticas

### ✅ Fazer

- Sempre verificar permissões antes de renderizar UI
- Validar permissões no backend (use cases)
- Usar permissões granulares
- Filtrar dados por empresa
- Logar ações importantes

### ❌ Evitar

- Confiar apenas em validações de frontend
- Expor dados de outras empresas
- Usar roles hardcoded ao invés de permissões
- Misturar lógica de autenticação com lógica de negócio

## Próximos Passos

### Produção

- [ ] Implementar hash de senhas
- [ ] Adicionar refresh tokens
- [ ] Implementar rate limiting
- [ ] Adicionar 2FA (autenticação de dois fatores)
- [ ] Logs de auditoria
- [ ] Política de expiração de senhas
- [ ] Bloqueio após tentativas falhas

### Features

- [ ] Convites por email
- [ ] Recuperação de senha
- [ ] Níveis de permissão customizáveis
- [ ] Grupos de usuários
- [ ] Delegação de permissões temporárias
