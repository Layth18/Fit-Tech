import { useState, useEffect } from 'react';
import { 
  Trophy, Target, 
  Calendar, AlertCircle, ChevronRight, Users, Award,
   Clock, MapPin
} from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const [user, setUser] = useState({ name: 'Demo User', email: 'demo@sports.com' });

  useEffect(() => {
    // Get user info from localStorage (Keycloak token)
    const userName = localStorage.getItem('user_name') || 'Demo User';
    setUser({ name: userName, email: 'demo@sports.com' });
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('keycloak_token');
    localStorage.removeItem('user_name');
    window.location.href = '/';
  };

  // Chart Data
  const performanceData = [
    { month: 'Jan', wins: 8, losses: 2 },
    { month: 'Feb', wins: 7, losses: 3 },
    { month: 'Mar', wins: 9, losses: 1 },
    { month: 'Apr', wins: 8, losses: 2 },
    { month: 'May', wins: 10, losses: 0 },
  ];

  const goalsData = [
    { week: 'W1', goals: 12, conceded: 5 },
    { week: 'W2', goals: 15, conceded: 7 },
    { week: 'W3', goals: 18, conceded: 4 },
    { week: 'W4', goals: 14, conceded: 6 },
  ];

  const recentActivity = [
    { type: 'match', title: 'Victory against Blue Thunder FC', time: '2 hours ago', icon: Trophy, color: 'text-green-400' },
    { type: 'training', title: 'Team training session completed', time: '5 hours ago', icon: Users, color: 'text-blue-400' },
    { type: 'injury', title: 'Player Mike Johnson - Knee injury update', time: '1 day ago', icon: AlertCircle, color: 'text-yellow-400' },
    { type: 'match', title: 'Match scheduled vs Red Dragons', time: '2 days ago', icon: Calendar, color: 'text-blue-400' },
  ];

  const alerts = [
    { title: 'Training schedule updated', desc: 'Morning session moved to 8:00 AM', priority: 'high' },
    { title: 'Upcoming match in 3 days', desc: 'vs Thunder United at Central Stadium', priority: 'medium' },
    { title: 'Equipment maintenance', desc: 'Gym equipment servicing tomorrow', priority: 'low' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-white mb-2">Welcome back, {user.name.split(' ')[0]}!</h2>
          <p className="text-slate-400">Here's your team performance overview</p>
        </div>

        {/* Top KPI Cards - F-Pattern Layout */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Last Match Result */}
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl hover:shadow-2xl transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-green-600/20 rounded-lg flex items-center justify-center">
                  <Trophy className="w-5 h-5 text-green-400" />
                </div>
                <h3 className="text-lg font-semibold text-white">Last Match</h3>
              </div>
              <span className="px-3 py-1 bg-green-600/20 text-green-400 text-xs font-semibold rounded-full">WIN</span>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold text-white">3 - 1</span>
                <span className="text-slate-400 text-sm">vs Blue Thunder FC</span>
              </div>
              <div className="flex items-center space-x-2 text-slate-400 text-sm">
                <Calendar className="w-4 h-4" />
                <span>May 5, 2025</span>
              </div>
              <div className="flex items-center space-x-2 text-slate-400 text-sm">
                <MapPin className="w-4 h-4" />
                <span>Home Stadium</span>
              </div>
            </div>
          </div>

          {/* Team Stats */}
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl hover:shadow-2xl transition-shadow">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-blue-600/20 rounded-lg flex items-center justify-center">
                <Target className="w-5 h-5 text-blue-400" />
              </div>
              <h3 className="text-lg font-semibold text-white">Team Stats</h3>
            </div>
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-400 text-sm">Win Ratio</span>
                  <span className="text-white font-semibold">82%</span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div className="bg-gradient-to-r from-blue-600 to-blue-400 h-2 rounded-full" style={{ width: '82%' }}></div>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4 pt-2">
                <div>
                  <p className="text-slate-400 text-xs mb-1">Goals For</p>
                  <p className="text-2xl font-bold text-green-400">59</p>
                </div>
                <div>
                  <p className="text-slate-400 text-xs mb-1">Goals Against</p>
                  <p className="text-2xl font-bold text-red-400">22</p>
                </div>
              </div>
            </div>
          </div>

          {/* Featured Player */}
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl hover:shadow-2xl transition-shadow">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-yellow-600/20 rounded-lg flex items-center justify-center">
                <Award className="w-5 h-5 text-yellow-400" />
              </div>
              <h3 className="text-lg font-semibold text-white">Player of the Week</h3>
            </div>
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-600 to-blue-800 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                JD
              </div>
              <div className="flex-1">
                <h4 className="text-white font-semibold">John Doe</h4>
                <p className="text-slate-400 text-sm mb-2">Forward</p>
                <div className="grid grid-cols-3 gap-2 text-center">
                  <div>
                    <p className="text-xs text-slate-400">Goals</p>
                    <p className="text-lg font-bold text-blue-400">5</p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-400">Assists</p>
                    <p className="text-lg font-bold text-blue-400">3</p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-400">Rating</p>
                    <p className="text-lg font-bold text-yellow-400">9.2</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Performance Chart */}
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-white">Win/Loss Performance</h3>
              <div className="flex items-center space-x-2">
                <div className="flex items-center space-x-1">
                  <div className="w-3 h-3 bg-blue-600 rounded-full"></div>
                  <span className="text-xs text-slate-400">Wins</span>
                </div>
                <div className="flex items-center space-x-1">
                  <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                  <span className="text-xs text-slate-400">Losses</span>
                </div>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="month" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '8px' }}
                  labelStyle={{ color: '#e2e8f0' }}
                />
                <Line type="monotone" dataKey="wins" stroke="#3b82f6" strokeWidth={3} dot={{ fill: '#3b82f6', r: 5 }} />
                <Line type="monotone" dataKey="losses" stroke="#ef4444" strokeWidth={3} dot={{ fill: '#ef4444', r: 5 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Goals Chart */}
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-white">Goals Overview</h3>
              <div className="flex items-center space-x-2">
                <div className="flex items-center space-x-1">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="text-xs text-slate-400">Scored</span>
                </div>
                <div className="flex items-center space-x-1">
                  <div className="w-3 h-3 bg-slate-400 rounded-full"></div>
                  <span className="text-xs text-slate-400">Conceded</span>
                </div>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={goalsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="week" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '8px' }}
                  labelStyle={{ color: '#e2e8f0' }}
                />
                <Bar dataKey="goals" fill="#22c55e" radius={[8, 8, 0, 0]} />
                <Bar dataKey="conceded" fill="#94a3b8" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Bottom Section - Activity & Alerts */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Recent Activity Feed */}
          <div className="lg:col-span-2 bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-white">Recent Activity</h3>
              <button className="text-blue-400 text-sm hover:text-blue-300 flex items-center space-x-1">
                <span>View All</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
            <div className="space-y-4">
              {recentActivity.map((activity, index) => (
                <div key={index} className="flex items-start space-x-4 p-4 bg-slate-800/50 rounded-xl hover:bg-slate-700/50 transition-colors">
                  <div className="w-10 h-10 bg-slate-700 rounded-lg flex items-center justify-center flex-shrink-0">
                    <activity.icon className={`w-5 h-5 ${activity.color}`} />
                  </div>
                  <div className="flex-1">
                    <p className="text-white font-medium mb-1">{activity.title}</p>
                    <div className="flex items-center space-x-2 text-slate-400 text-sm">
                      <Clock className="w-3 h-3" />
                      <span>{activity.time}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Alerts Panel */}
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-yellow-600/20 rounded-lg flex items-center justify-center">
                <AlertCircle className="w-5 h-5 text-yellow-400" />
              </div>
              <h3 className="text-lg font-semibold text-white">Alerts</h3>
            </div>
            <div className="space-y-3">
              {alerts.map((alert, index) => (
                <div 
                  key={index} 
                  className={`p-4 rounded-xl border ${
                    alert.priority === 'high' 
                      ? 'bg-red-600/10 border-red-600/30' 
                      : alert.priority === 'medium'
                      ? 'bg-yellow-600/10 border-yellow-600/30'
                      : 'bg-blue-600/10 border-blue-600/30'
                  }`}
                >
                  <h4 className="text-white font-medium text-sm mb-1">{alert.title}</h4>
                  <p className="text-slate-400 text-xs">{alert.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;