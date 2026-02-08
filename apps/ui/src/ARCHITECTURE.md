# Arquitetura do Projeto - Clean Architecture

## Visão Geral

Este projeto segue os princípios do **Clean Architecture** (Arquitetura Limpa), proposto por Robert C. Martin (Uncle Bob). A arquitetura está organizada em camadas concêntricas, onde as dependências sempre apontam para dentro, garantindo independência de frameworks, testabilidade e manutenibilidade.

## Estrutura de Pastas

```
/
├── domain/                    # Camada de Domínio (regras de negócio)
│   ├── entities/             # Entidades de negócio
│   │   ├── Conversation.ts
│   │   ├── Message.ts
│   │   ├── Attendant.ts
│   │   └── Metrics.ts
│   ├── repositories/         # Interfaces dos repositórios (contratos)
│   │   ├── IConversationRepository.ts
│   │   └── IMetricsRepository.ts
│   └── use-cases/           # Casos de uso (lógica de aplicação)
│       ├── GetConversations.ts
│       ├── GetConversationMessages.ts
│       ├── AssignConversationToAttendant.ts
│       ├── SendMessage.ts
│       ├── GetAttendants.ts
│       └── GetDashboardMetrics.ts
│
├── data/                     # Camada de Dados
│   └── repositories/        # Implementações dos repositórios
│       ├── ConversationRepository.ts
│       └── MetricsRepository.ts
│
├── infrastructure/          # Camada de Infraestrutura
│   └── di/                 # Dependency Injection (Injeção de Dependências)
│       └── container.ts    # Container DI com configuração de dependências
│
├── presentation/           # Camada de Apresentação (UI)
│   ├── components/        # Componentes React
│   │   ├── Sidebar.tsx
│   │   ├── ConversationList.tsx
│   │   ├── ChatArea.tsx
│   │   ├── AttendantPanel.tsx
│   │   └── Dashboard.tsx
│   └── hooks/            # Custom Hooks (conectam UI com Use Cases)
│       ├── useConversations.ts
│       ├── useConversationMessages.ts
│       ├── useAttendants.ts
│       └── useMetrics.ts
│
├── components/ui/        # Componentes UI base (ShadCN)
└── App.tsx              # Componente principal da aplicação
```

## Camadas da Arquitetura

### 1. Domain (Domínio) - Núcleo da Aplicação

**Responsabilidade**: Contém as regras de negócio e lógica da aplicação. Não depende de nada externo.

#### Entities (Entidades)

- Modelos de dados puros que representam conceitos do domínio
- Exemplos: `Conversation`, `Message`, `Attendant`, `Metrics`
- Sem dependências externas

#### Use Cases (Casos de Uso)

- Implementam a lógica de negócio da aplicação
- Orquestram o fluxo de dados entre repositories e apresentação
- Cada use case representa uma ação do usuário
- Exemplos: `GetConversations`, `AssignConversationToAttendant`

#### Repositories (Interfaces)

- Definem contratos (interfaces) para acesso a dados
- Não implementam lógica, apenas definem o que deve ser feito
- Seguem o padrão Repository Pattern

### 2. Data (Dados)

**Responsabilidade**: Implementa os contratos definidos na camada de domínio.

- Implementações concretas dos repositórios
- Atualmente usa dados mock em memória
- Pode ser facilmente substituído por implementações reais (API REST, GraphQL, etc.)

### 3. Infrastructure (Infraestrutura)

**Responsabilidade**: Configuração e setup de dependências.

#### Dependency Injection Container

- Centraliza a criação e configuração de todas as dependências
- Instancia repositórios e use cases
- Facilita testes e manutenção
- Ponto único para trocar implementações

### 4. Presentation (Apresentação)

**Responsabilidade**: Interface do usuário e interação com o usuário.

#### Components (Componentes)

- Componentes React que renderizam a UI
- Focados apenas em apresentação
- Não contêm lógica de negócio

#### Hooks (Custom Hooks)

- Conectam os componentes UI com os use cases
- Gerenciam estado local da UI
- Fazem a ponte entre a camada de apresentação e domínio

## Fluxo de Dados

```
User Interaction
      ↓
Component (presentation/components/)
      ↓
Custom Hook (presentation/hooks/)
      ↓
Use Case (domain/use-cases/)
      ↓
Repository Interface (domain/repositories/)
      ↓
Repository Implementation (data/repositories/)
      ↓
Data Source (Mock/API)
```

## Princípios Aplicados

### 1. Dependency Rule (Regra de Dependência)

- As dependências sempre apontam para dentro
- Domain não depende de nada
- Data depende de Domain
- Presentation depende de Domain (através dos hooks)

### 2. Separation of Concerns (Separação de Responsabilidades)

- Cada camada tem uma responsabilidade bem definida
- Facilita manutenção e evolução do código

### 3. Dependency Inversion Principle (DIP)

- Use cases dependem de interfaces (abstrações), não de implementações
- Fácil substituir implementações sem afetar a lógica de negócio

### 4. Single Responsibility Principle (SRP)

- Cada classe/módulo tem uma única responsabilidade
- Use cases são pequenos e focados

## Vantagens desta Arquitetura

### ✅ Testabilidade

- Fácil testar cada camada isoladamente
- Use cases podem ser testados sem UI
- Repositórios podem ser mockados

### ✅ Independência de Framework

- Lógica de negócio não depende de React, API, ou banco de dados
- Fácil migrar para outra tecnologia de UI

### ✅ Manutenibilidade

- Código organizado e fácil de entender
- Mudanças em uma camada não afetam outras

### ✅ Escalabilidade

- Fácil adicionar novos casos de uso
- Fácil trocar implementações de repositórios

### ✅ Flexibilidade

- Dados mock podem ser facilmente substituídos por APIs reais
- Múltiplas implementações do mesmo repositório (cache, API, local storage)

## Como Adicionar Novas Funcionalidades

### 1. Nova Entidade

```typescript
// domain/entities/NewEntity.ts
export interface NewEntity {
  id: string;
  // ... propriedades
}
```

### 2. Novo Repositório

```typescript
// domain/repositories/INewRepository.ts
export interface INewRepository {
  getAll(): Promise<NewEntity[]>;
}

// data/repositories/NewRepository.ts
export class NewRepository implements INewRepository {
  async getAll(): Promise<NewEntity[]> {
    // implementação
  }
}
```

### 3. Novo Use Case

```typescript
// domain/use-cases/GetNewEntities.ts
export class GetNewEntities {
  constructor(private repository: INewRepository) {}

  async execute(): Promise<NewEntity[]> {
    return await this.repository.getAll();
  }
}
```

### 4. Registrar no Container DI

```typescript
// infrastructure/di/container.ts
const newRepository = new NewRepository();
export const getNewEntitiesUseCase = new GetNewEntities(newRepository);
```

### 5. Criar Hook

```typescript
// presentation/hooks/useNewEntities.ts
export function useNewEntities() {
  const [entities, setEntities] = useState<NewEntity[]>([]);

  useEffect(() => {
    const loadEntities = async () => {
      const data = await getNewEntitiesUseCase.execute();
      setEntities(data);
    };
    loadEntities();
  }, []);

  return { entities };
}
```

### 6. Usar no Componente

```typescript
// presentation/components/NewComponent.tsx
export function NewComponent() {
  const { entities } = useNewEntities();

  return (
    <div>
      {entities.map(entity => (
        <div key={entity.id}>{/* render */}</div>
      ))}
    </div>
  );
}
```

## Substituindo Dados Mock por API Real

Para conectar a uma API real do WhatsApp:

1. Criar nova implementação do repositório:

```typescript
// data/repositories/WhatsAppConversationRepository.ts
export class WhatsAppConversationRepository implements IConversationRepository {
  async getAll(): Promise<Conversation[]> {
    const response = await fetch("/api/conversations");
    return response.json();
  }
  // ... outros métodos
}
```

2. Atualizar o container DI:

```typescript
// infrastructure/di/container.ts
const conversationRepository = new WhatsAppConversationRepository();
// ao invés de: new ConversationRepository();
```

**Nenhuma outra mudança é necessária!** Os use cases, hooks e componentes continuam funcionando sem alteração.

## Conclusão

Esta arquitetura garante que o projeto seja:

- **Limpo**: Código organizado e fácil de entender
- **Testável**: Fácil escrever testes unitários e de integração
- **Flexível**: Fácil adicionar ou modificar funcionalidades
- **Manutenível**: Mudanças isoladas em camadas específicas
- **Escalável**: Preparado para crescer com novos requisitos

A separação clara de responsabilidades e o uso de interfaces tornam o código resiliente a mudanças e fácil de evoluir ao longo do tempo.
