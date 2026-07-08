import {
  Navigate,
  useLocation
} from "react-router-dom";

import {
  useAuth
} from "../auth/AuthContext.jsx";


function ProtectedRoute({
  children,
  requiredPermission = null,
  requiredPermissions = []
}) {
  const {
    user,
    loading,
    hasAnyPermission
  } = useAuth();

  const location = useLocation();


  const permissionsToCheck = [
    ...(requiredPermission
      ? [requiredPermission]
      : []),

    ...requiredPermissions
  ];


  if (loading) {
    return (
      <main className="container">
        <section className="card">
          <p>
            Verificando sesión...
          </p>
        </section>
      </main>
    );
  }


  if (!user) {
    return (
      <Navigate
        to="/login"
        state={{
          from: location
        }}
        replace
      />
    );
  }


  if (
    permissionsToCheck.length > 0 &&
    !hasAnyPermission(
      ...permissionsToCheck
    )
  ) {
    return (
      <Navigate
        to="/"
        replace
      />
    );
  }


  return children;
}


export default ProtectedRoute;