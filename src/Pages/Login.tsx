import React, { useState } from 'react';
import { Shield, TrendingUp, Activity, BarChart3 } from 'lucide-react';

// Keycloak Configuration (Replace with your actual Keycloak settings)
const KEYCLOAK_CONFIG = {
  url: 'https://your-keycloak-domain.com/auth',
  realm: 'sports-analytics',
  clientId: 'sports-platform',
  redirectUri: window.location.origin + '/app'
};

const LoginPage = () => {
  const [isAuthenticating, setIsAuthenticating] = useState(false);

  const handleKeycloakLogin = () => {
    setIsAuthenticating(true);

    // Construct Keycloak login URL
    const keycloakLoginUrl = `${KEYCLOAK_CONFIG.url}/realms/${KEYCLOAK_CONFIG.realm}/protocol/openid-connect/auth?client_id=${KEYCLOAK_CONFIG.clientId}&redirect_uri=${encodeURIComponent(KEYCLOAK_CONFIG.redirectUri)}&response_type=code&scope=openid`;

    // Redirect to Keycloak login
    // For demo purposes, we'll simulate authentication
    setTimeout(() => {
      const mockToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...';
      localStorage.setItem('keycloak_token', mockToken);
      localStorage.setItem('user_name', 'Demo User');
      window.location.href = '/app';
    }, 1500);

    // Uncomment for real Keycloak integration:
    // window.location.href = keycloakLoginUrl;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-20 left-20 w-64 h-64 bg-blue-600 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-slate-400 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>

      {/* Login Card */}
      <div className="relative z-10 w-full max-w-md">
        <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl shadow-2xl border border-slate-700/50 p-8 space-y-8">
          
          {/* Logo and Title */}
          <div className="text-center space-y-4">
            <div className="flex justify-center">
              <div className="relative">
                <div className="w-20 h-20 bg-gradient-to-br from-blue-600 to-blue-800 rounded-full flex items-center justify-center shadow-lg">
                  <TrendingUp className="w-10 h-10 text-white" strokeWidth={2.5} />
                </div>
                <div className="absolute -bottom-1 -right-1 w-6 h-6 bg-slate-400 rounded-full flex items-center justify-center">
                  <Activity className="w-4 h-4 text-slate-900" strokeWidth={3} />
                </div>
              </div>
            </div>

            <div>
              <h1 className="text-3xl font-bold text-white mb-2">
                Sports Analytics
              </h1>
              <p className="text-slate-400 text-sm">
                Professional Performance Tracking Platform
              </p>
            </div>
          </div>

          {/* Feature Icons */}
          <div className="grid grid-cols-3 gap-4 py-6 border-y border-slate-700/50">
            <div className="text-center space-y-2">
              <div className="w-12 h-12 mx-auto bg-blue-600/20 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-blue-400" />
              </div>
              <p className="text-xs text-slate-400">Analytics</p>
            </div>
            <div className="text-center space-y-2">
              <div className="w-12 h-12 mx-auto bg-blue-600/20 rounded-lg flex items-center justify-center">
                <Activity className="w-6 h-6 text-blue-400" />
              </div>
              <p className="text-xs text-slate-400">Real-time</p>
            </div>
            <div className="text-center space-y-2">
              <div className="w-12 h-12 mx-auto bg-blue-600/20 rounded-lg flex items-center justify-center">
                <Shield className="w-6 h-6 text-blue-400" />
              </div>
              <p className="text-xs text-slate-400">Secure</p>
            </div>
          </div>

          {/* Login Button */}
          <button
            onClick={handleKeycloakLogin}
            disabled={isAuthenticating}
            className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-200 flex items-center justify-center space-x-3 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed group"
          >
            {isAuthenticating ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Authenticating...</span>
              </>
            ) : (
              <>
                <Shield className="w-5 h-5 group-hover:scale-110 transition-transform" />
                <span>Sign in with Keycloak</span>
              </>
            )}
          </button>

          {/* Security Notice */}
          <div className="text-center space-y-2">
            <p className="text-xs text-slate-500">
              Secured by Keycloak Authentication
            </p>
            <div className="flex items-center justify-center space-x-1 text-slate-600">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-xs">End-to-end encrypted</span>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-6 text-slate-500 text-sm">
          <p>© 2025 Sports Analytics Platform. All rights reserved.</p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
