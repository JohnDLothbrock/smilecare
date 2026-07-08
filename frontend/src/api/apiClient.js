const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000"
).replace(
  /\/+$/,
  ""
);


let accessToken = null;


async function request(
  endpoint,
  options = {}
) {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {})
  };


  if (accessToken) {
    headers.Authorization =
      `Bearer ${accessToken}`;
  }


  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      ...options,
      headers
    }
  );


  const data = await response
    .json()
    .catch(() => null);


  if (!response.ok) {
    if (
      response.status === 401 &&
      endpoint !== "/auth/login"
    ) {
      window.dispatchEvent(
        new Event(
          "smilecare:unauthorized"
        )
      );
    }


    const message =
      data?.detail ||
      "Ocurrió un error al comunicarse con el servidor.";


    throw new Error(message);
  }


  return data;
}


export const apiClient = {
  setAccessToken(token) {
    accessToken = token || null;
  },


  clearAccessToken() {
    accessToken = null;
  },


  get(endpoint) {
    return request(endpoint);
  },


  post(endpoint, body) {
    return request(
      endpoint,
      {
        method: "POST",
        body: JSON.stringify(body)
      }
    );
  },


  put(endpoint, body) {
    return request(
      endpoint,
      {
        method: "PUT",
        body: JSON.stringify(body)
      }
    );
  },


  delete(endpoint) {
    return request(
      endpoint,
      {
        method: "DELETE"
      }
    );
  }
};