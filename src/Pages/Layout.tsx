import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, LogOut, Bell, Menu, X, Home, Trophy, 
  Users, GitCompare, FileText, ChevronRight
} from 'lucide-react';

// Import your existing page components
import LoginPage from './Login';
import PlayersPage from './Players';
import PDFPage from './PDF';
import ComparisionPage from './Comparision';
import Dashboard from './Dashboard';
import MatchesPage from './Matches';

const GlobalLayout = () => {
  const [user, setUser] = useState({ name: 'Demo User', email: 'demo@sports.com' });
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isInitialLoad, setIsInitialLoad] = useState(true);
  const [notifications] = useState(3);

  useEffect(() => {
    // Check authentication on mount
    const token = localStorage.getItem('keycloak_token');
    
    if (!token) {
      setIsAuthenticated(false);
      setIsInitialLoad(false);
    } else {
      // Show initial loading screen
      setTimeout(() => {
        const userName = localStorage.getItem('user_name') || 'Demo User';
        setUser({ name: userName, email: 'demo@sports.com' });
        setIsAuthenticated(true);
        setIsInitialLoad(false);
      }, 2500);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('keycloak_token');
    localStorage.removeItem('user_name');
    setIsAuthenticated(false);
    setCurrentPage('dashboard');
  };

  const handleLogin = () => {
    // Called after successful login from LoginPage
    const userName = localStorage.getItem('user_name') || 'Demo User';
    setUser({ name: userName, email: 'demo@sports.com' });
    setIsAuthenticated(true);
  };

  const handlePageChange = (page) => {
    if (currentPage === page) return;
    setCurrentPage(page);
    setIsSidebarOpen(false);
  };

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'matches', label: 'Matches', icon: Trophy },
    { id: 'players', label: 'Players', icon: Users },
    { id: 'comparison', label: 'Comparison', icon: GitCompare },
    { id: 'reports', label: 'Reports', icon: FileText },
  ];

  const renderPageContent = () => {
    const pageMap = {
      dashboard: <Dashboard />,
      matches: <MatchesPage />,
      players: <PlayersPage />,
      comparison: <ComparisionPage />,
      reports: <PDFPage />,
    };

    return pageMap[currentPage] || <Dashboard />;
  };



  // Show login page if not authenticated
  if (!isAuthenticated) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <style>{`
        @keyframes slide-in-left {
          from {
            transform: translateX(-100%);
          }
          to {
            transform: translateX(0);
          }
        }

        .slide-in-left {
          animation: slide-in-left 0.3s ease-out;
        }
      `}</style>

      {/* Sidebar - Desktop (Always Visible) */}
      <aside className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col z-40">
        <div className="flex flex-col flex-grow bg-slate-900/95 backdrop-blur-lg border-r border-slate-700/50 overflow-y-auto">
          {/* Logo */}
          <div className="flex items-center space-x-3 px-6 py-6 border-b border-slate-700/50">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center shadow-lg">
              <TrendingUp className="w-6 h-6 text-white" strokeWidth={2.5} />
            </div>
            <div>
              <h1 className="text-lg font-bold text-white">Sports Analytics</h1>
              <p className="text-xs text-slate-400">Performance Platform</p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            {menuItems.map((item) => (
              <button
                key={item.id}
                onClick={() => handlePageChange(item.id)}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all ${
                  currentPage === item.id
                    ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
                {currentPage === item.id && <ChevronRight className="w-4 h-4 ml-auto" />}
              </button>
            ))}
          </nav>

          {/* User Info - Sidebar */}
          <div className="px-4 py-4 border-t border-slate-700/50">
            <div className="flex items-center space-x-3 px-4 py-3 bg-slate-800/50 rounded-xl">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-700 rounded-full flex items-center justify-center text-white font-semibold">
                {user.name.charAt(0)}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">{user.name}</p>
                <p className="text-xs text-slate-400 truncate">{user.email}</p>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* Mobile Sidebar Overlay */}
      {isSidebarOpen && (
        <div className="lg:hidden fixed inset-0 z-40 bg-black/60 backdrop-blur-sm" onClick={() => setIsSidebarOpen(false)}>
          <aside className="fixed inset-y-0 left-0 w-64 bg-slate-900/95 backdrop-blur-lg border-r border-slate-700/50 slide-in-left" onClick={(e) => e.stopPropagation()}>
            <div className="flex flex-col h-full">
              {/* Logo */}
              <div className="flex items-center justify-between px-6 py-6 border-b border-slate-700/50">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center shadow-lg">
                    <TrendingUp className="w-6 h-6 text-white" strokeWidth={2.5} />
                  </div>
                  <div>
                    <h1 className="text-lg font-bold text-white">Sports Analytics</h1>
                    <p className="text-xs text-slate-400">Performance Platform</p>
                  </div>
                </div>
                <button onClick={() => setIsSidebarOpen(false)} className="p-2 hover:bg-slate-800 rounded-lg transition-colors">
                  <X className="w-5 h-5 text-slate-400" />
                </button>
              </div>

              {/* Navigation */}
              <nav className="flex-1 px-4 py-6 space-y-2">
                {menuItems.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => handlePageChange(item.id)}
                    className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all ${
                      currentPage === item.id
                        ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg'
                        : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                    }`}
                  >
                    <item.icon className="w-5 h-5" />
                    <span className="font-medium">{item.label}</span>
                    {currentPage === item.id && <ChevronRight className="w-4 h-4 ml-auto" />}
                  </button>
                ))}
              </nav>

              {/* User Info */}
              <div className="px-4 py-4 border-t border-slate-700/50">
                <div className="flex items-center space-x-3 px-4 py-3 bg-slate-800/50 rounded-xl">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-700 rounded-full flex items-center justify-center text-white font-semibold">
                    {user.name.charAt(0)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-white truncate">{user.name}</p>
                    <p className="text-xs text-slate-400 truncate">{user.email}</p>
                  </div>
                </div>
              </div>
            </div>
          </aside>
        </div>
      )}

      {/* Main Content */}
      <div className="lg:pl-64 flex flex-col min-h-screen">
        {/* Top Bar */}
        <header className="bg-slate-800/80 backdrop-blur-lg border-b border-slate-700/50 sticky top-0 z-30">
          <div className="px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              {/* Mobile Menu Button */}
              <button
                onClick={() => setIsSidebarOpen(true)}
                className="lg:hidden p-2 text-slate-400 hover:text-white hover:bg-slate-700/50 rounded-lg transition-colors"
              >
                <Menu className="w-6 h-6" />
              </button>

              {/* Page Title - Mobile */}
              <div className="lg:hidden">
                <h2 className="text-lg font-bold text-white capitalize">{currentPage}</h2>
              </div>

              {/* Right Side */}
              <div className="flex items-center space-x-4 ml-auto">
                {/* Notifications */}
                <button className="relative p-2 text-slate-400 hover:text-white hover:bg-slate-700/50 rounded-lg transition-colors">
                  <Bell className="w-5 h-5" />
                  {notifications > 0 && (
                    <span className="absolute top-1 right-1 w-4 h-4 bg-blue-600 text-white text-xs rounded-full flex items-center justify-center">
                      {notifications}
                    </span>
                  )}
                </button>

                {/* User Avatar - Desktop */}
                <div className="hidden lg:flex items-center space-x-3 px-3 py-2 bg-slate-700/50 rounded-lg">
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-700 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                    {user.name.charAt(0)}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-white">{user.name}</p>
                    <p className="text-xs text-slate-400">{user.email}</p>
                  </div>
                </div>

                {/* Logout Button */}
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-2 px-4 py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 hover:text-red-300 rounded-lg transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  <span className="hidden sm:inline text-sm font-medium">Logout</span>
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1">
          {renderPageContent()}
        </main>
      </div>
    </div>
  );
};

export default GlobalLayout;