# Domain Layer (Camada de Domínio)

Esta é a camada mais interna da aplicação. Contém as **regras de negócio** e é completamente independente de frameworks, UI, banco de dados ou qualquer detalhe externo.

## Estrutura

### 📦 Entities (Entidades)

Modelos de dados puros que representam os conceitos centrais do domínio.

- **Conversation**: Representa uma conversa com um cliente
- **Message**: Representa uma mensagem individual
- **Attendant**: Representa um atendente do sistema
- **Metrics**: Representa métricas e KPIs do dashboard

### 🔌 Repositories (Interfaces)

Contratos que definem como acessar dados. Apenas interfaces, sem implementação.

- **IConversationRepository**: Contrato para gerenciar conversas
- **IMetricsRepository**: Contrato para obter métricas

### ⚙️ Use Cases (Casos de Uso)

Implementam a lógica de negócio da aplicação. Cada use case representa uma ação específica.

- **GetConversations**: Obtém todas as conversas
- **GetConversationMessages**: Obtém mensagens de uma conversa
- **AssignConversationToAttendant**: Atribui uma conversa a um atendente
- **SendMessage**: Envia uma mensagem
- **GetAttendants**: Obtém todos os atendentes
- **GetDashboardMetrics**: Obtém métricas do dashboard

## Regras Importantes

### ✅ Permitido

- Definir modelos de dados (entities)
- Definir contratos de repositórios (interfaces)
- Implementar lógica de negócio (use cases)
- Use cases podem usar entities e repository interfaces

### ❌ Não Permitido

- Importar bibliotecas de UI (React, etc.)
- Importar bibliotecas de HTTP (fetch, axios)
- Importar implementações de repositórios
- Ter dependências externas

## Exemplo de Use Case

```typescript
export class AssignConversationToAttendant {
  constructor(private conversationRepository: IConversationRepository) {}

  async execute(conversationId: string, attendantName: string | null): Promise<void> {
    // Validação de regra de negócio
    if (conversationId.trim() === "") {
      throw new Error("ID da conversa é obrigatório");
    }

    // Delega a persistência para o repositório
    await this.conversationRepository.assignAttendant(conversationId, attendantName);
  }
}
```

Note que:

1. O use case recebe o repositório via construtor (Dependency Injection)
2. Contém validação de regra de negócio
3. Não sabe COMO os dados são salvos (pode ser API, mock, banco local, etc.)
4. É fácil de testar (pode usar um repositório fake/mock)
