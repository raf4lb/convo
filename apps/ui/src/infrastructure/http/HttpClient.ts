export type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
export type HttpHeaders = Record<string, string>;

export type HttpResponse = {
  status: number;
  data: unknown;
};

export type RequestInterceptor = (
  url: string,
  init: RequestInit,
) => Promise<{ url: string; init: RequestInit }>;

export type ResponseInterceptor = (response: Response) => Promise<Response>;

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

type QueryParams = Record<string, string | number | boolean | undefined>;

interface RequestOptions {
  headers?: HttpHeaders;
  query?: QueryParams;
}

interface RequestOptionsWithBody extends RequestOptions {
  body?: unknown;
}

export class HttpClient {
  private readonly defaultHeaders: HttpHeaders;
  private requestInterceptors: RequestInterceptor[] = [];
  private responseInterceptors: ResponseInterceptor[] = [];

  constructor(
    private readonly baseUrl: string,
    private readonly timeoutMs = 5000,
    private readonly maxRetries = 2,
    defaultHeaders: HttpHeaders = {},
  ) {
    this.defaultHeaders = {
      "Content-Type": "application/json",
      ...defaultHeaders,
    };
  }

  addRequestInterceptor(interceptor: RequestInterceptor): void {
    this.requestInterceptors.push(interceptor);
  }

  addResponseInterceptor(interceptor: ResponseInterceptor): void {
    this.responseInterceptors.push(interceptor);
  }

  /**
   * Executes fetch with timeout support using AbortController.
   */
  private async fetchWithTimeout(url: string, options: RequestInit): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      let modifiedUrl = url;
      let modifiedOptions = { ...options, signal: controller.signal };

      for (const interceptor of this.requestInterceptors) {
        const result = await interceptor(modifiedUrl, modifiedOptions);
        modifiedUrl = result.url;
        modifiedOptions = result.init;
      }

      let response = await fetch(modifiedUrl, modifiedOptions);

      for (const interceptor of this.responseInterceptors) {
        response = await interceptor(response);
      }

      return response;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  /**
   * Core request handler with retry and error throwing.
   */
  private async request(
    method: HttpMethod,
    path: string,
    options?: {
      body?: unknown;
      headers?: HttpHeaders;
      query?: Record<string, string | number | boolean | undefined>;
    },
    attempt = 0,
  ): Promise<HttpResponse> {
    const url = new URL(path, this.baseUrl);

    if (options?.query) {
      Object.entries(options.query).forEach(([key, value]) => {
        if (value !== undefined) {
          url.searchParams.append(key, String(value));
        }
      });
    }

    try {
      const response = await this.fetchWithTimeout(url.toString(), {
        method,
        headers: {
          ...this.defaultHeaders,
          ...options?.headers,
        },
        body: options?.body && method !== "GET" ? JSON.stringify(options.body) : undefined,
        credentials: "include",
      });

      const data = await response.json().catch(() => null);

      if (!response.ok && response.status !== 404) {
        throw new Error(`HTTP ${response.status}: ${JSON.stringify(data)}`);
      }

      return {
        status: response.status,
        data,
      };
    } catch (error: any) {
      // Retry only for network / timeout errors
      if (attempt < this.maxRetries && this.isRetryableError(error)) {
        const backoffMs = 2 ** attempt * 100;
        await sleep(backoffMs);
        return this.request(method, path, options, attempt + 1);
      }

      throw error instanceof Error ? error : new Error(String(error));
    }
  }

  /**
   * Defines which errors are eligible for retry.
   */
  private isRetryableError(error: unknown): boolean {
    if (!(error instanceof Error)) return false;

    // AbortError (timeout) or generic network failure
    return error.name === "AbortError" || error.message.includes("Network");
  }

  get(path: string, options?: RequestOptions): Promise<HttpResponse> {
    return this.request("GET", path, {
      headers: options?.headers,
      query: options?.query,
    });
  }

  post(path: string, options?: RequestOptionsWithBody): Promise<HttpResponse> {
    return this.request("POST", path, {
      body: options?.body,
      headers: options?.headers,
      query: options?.query,
    });
  }

  put(path: string, options?: RequestOptionsWithBody): Promise<HttpResponse> {
    return this.request("PUT", path, {
      body: options?.body,
      headers: options?.headers,
      query: options?.query,
    });
  }

  patch(path: string, options?: RequestOptionsWithBody): Promise<HttpResponse> {
    return this.request("PATCH", path, {
      body: options?.body,
      headers: options?.headers,
      query: options?.query,
    });
  }

  delete(path: string, options?: RequestOptions): Promise<HttpResponse> {
    return this.request("DELETE", path, {
      headers: options?.headers,
      query: options?.query,
    });
  }
}
