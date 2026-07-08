import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState
} from "react";

import {
  apiClient
} from "../api/apiClient.js";


const AuthContext =
  createContext(null);


const TOKEN_STORAGE_KEY =
  "smilecare_access_token";


export function AuthProvider({
  children
}) {
  const [user, setUser] =
    useState(null);

  const [loading, setLoading] =
    useState(true);


  const clearSession =
    useCallback(
      () => {
        localStorage.removeItem(
          TOKEN_STORAGE_KEY
        );

        apiClient.clearAccessToken();

        setUser(null);
      },
      []
    );


  useEffect(() => {
    async function restoreSession() {
      const storedToken =
        localStorage.getItem(
          TOKEN_STORAGE_KEY
        );


      if (!storedToken) {
        setLoading(false);
        return;
      }


      try {
        apiClient.setAccessToken(
          storedToken
        );

        const currentUser =
          await apiClient.get(
            "/auth/me"
          );

        setUser(currentUser);

      } catch {
        clearSession();

      } finally {
        setLoading(false);
      }
    }


    restoreSession();

  }, [clearSession]);


  useEffect(() => {
    function handleUnauthorized() {
      clearSession();
    }


    window.addEventListener(
      "smilecare:unauthorized",
      handleUnauthorized
    );


    return () => {
      window.removeEventListener(
        "smilecare:unauthorized",
        handleUnauthorized
      );
    };

  }, [clearSession]);


  const login = useCallback(
    async (
      nombreUsuario,
      password
    ) => {
      clearSession();


      const response =
        await apiClient.post(
          "/auth/login",
          {
            nombre_usuario:
              nombreUsuario,

            password
          }
        );


      const token =
        response.access_token;


      if (!token) {
        throw new Error(
          "El servidor no devolvió "
          + "un token de acceso."
        );
      }


      localStorage.setItem(
        TOKEN_STORAGE_KEY,
        token
      );


      apiClient.setAccessToken(
        token
      );


      try {
        const currentUser =
          await apiClient.get(
            "/auth/me"
          );

        setUser(currentUser);

        return currentUser;

      } catch (error) {
        clearSession();

        throw error;
      }
    },
    [clearSession]
  );


  const logout = useCallback(
    async () => {
      try {
        if (user) {
          await apiClient.post(
            "/auth/logout",
            {}
          );
        }

      } catch {
        // The local session is cleared
        // even if logout auditing fails.

      } finally {
        clearSession();
      }
    },
    [
      user,
      clearSession
    ]
  );


  const hasPermission =
    useCallback(
      (permissionCode) => {
        if (!user) {
          return false;
        }

        return (
          user.permisos || []
        ).includes(
          permissionCode
        );
      },
      [user]
    );


  const hasAnyPermission =
    useCallback(
      (...permissionCodes) => {
        if (!user) {
          return false;
        }


        const userPermissions =
          user.permisos || [];


        return permissionCodes.some(
          (permissionCode) =>
            userPermissions.includes(
              permissionCode
            )
        );
      },
      [user]
    );


  const value = useMemo(
    () => ({
      user,
      loading,

      isAuthenticated:
        user !== null,

      login,
      logout,

      hasPermission,
      hasAnyPermission
    }),
    [
      user,
      loading,
      login,
      logout,
      hasPermission,
      hasAnyPermission
    ]
  );


  return (
    <AuthContext.Provider
      value={value}
    >
      {children}
    </AuthContext.Provider>
  );
}


export function useAuth() {
  const context =
    useContext(AuthContext);


  if (!context) {
    throw new Error(
      "useAuth debe utilizarse "
      + "dentro de AuthProvider."
    );
  }


  return context;
}