import { ResponseInterceptor } from "./HttpClient";

/**
 * Auth interceptor that handles 401 responses by refreshing tokens.
 */
export class AuthInterceptor {
  private isRefreshing = false;
  private refreshPromise: Promise<boolean> | null = null;

  constructor(private readonly baseUrl: string) {}

  /**
   * Refresh the access token by calling /auth/refresh.
   */
  private async refreshToken(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/auth/refresh`, {
        method: "POST",
        credentials: "include",
      });

      return response.ok;
    } catch (error) {
      console.error("Token refresh failed:", error);
      return false;
    }
  }

  /**
   * Create a response interceptor that handles 401 errors.
   */
  createResponseInterceptor(): ResponseInterceptor {
    return async (response: Response): Promise<Response> => {
      if (response.status !== 401) {
        return response;
      }

      if (this.isRefreshing) {
        await this.refreshPromise;
        return response;
      }

      this.isRefreshing = true;
      this.refreshPromise = this.refreshToken();

      const refreshSuccess = await this.refreshPromise;

      this.isRefreshing = false;
      this.refreshPromise = null;

      if (refreshSuccess) {
        const originalRequest = response.clone();
        const retryResponse = await fetch(originalRequest.url, {
          method: originalRequest.headers.get("x-original-method") || "GET",
          headers: originalRequest.headers,
          credentials: "include",
        });
        return retryResponse;
      }

      return response;
    };
  }
}
