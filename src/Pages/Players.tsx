import React, { useState } from 'react';
import { 
  TrendingUp, LogOut, Bell, Search, Filter, User, MapPin, 
  Calendar, Trophy, Target, Activity, Clock, X, ArrowLeft,
  Award, TrendingDown, Users, Flag, ChevronRight, Heart,
  Weight, Ruler, CheckCircle, XCircle, AlertCircle
} from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const PlayersPage = () => {
  const [user] = useState({ name: 'Demo User', email: 'demo@sports.com' });
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    position: 'all',
    status: 'all'
  });

  const players = [
    { 
      id: 1, name: 'John Doe', position: 'Forward', status: 'Active', 
      photo: 'JD', age: 25, height: '6\'2"', weight: '180 lbs', nationality: '🇺🇸 USA',
      careerGoals: 127, careerAssists: 45, careerMatches: 210,
      seasonGoals: 18, seasonAssists: 7, seasonMatches: 24, rating: 8.9
    },
    { 
      id: 2, name: 'Mike Smith', position: 'Midfielder', status: 'Active',
      photo: 'MS', age: 27, height: '5\'11"', weight: '170 lbs', nationality: '🇬🇧 UK',
      careerGoals: 45, careerAssists: 89, careerMatches: 180,
      seasonGoals: 6, seasonAssists: 12, seasonMatches: 22, rating: 8.5
    },
    { 
      id: 3, name: 'Tom Brown', position: 'Defender', status: 'Active',
      photo: 'TB', age: 29, height: '6\'0"', weight: '185 lbs', nationality: '🇨🇦 Canada',
      careerGoals: 12, careerAssists: 23, careerMatches: 250,
      seasonGoals: 2, seasonAssists: 3, seasonMatches: 25, rating: 8.3
    },
    { 
      id: 4, name: 'Alex Johnson', position: 'Goalkeeper', status: 'Active',
      photo: 'AJ', age: 30, height: '6\'3"', weight: '190 lbs', nationality: '🇦🇺 Australia',
      careerGoals: 0, careerAssists: 2, careerMatches: 200,
      seasonGoals: 0, seasonAssists: 0, seasonMatches: 24, rating: 8.6
    },
    { 
      id: 5, name: 'Chris Lee', position: 'Forward', status: 'Injured',
      photo: 'CL', age: 23, height: '5\'10"', weight: '165 lbs', nationality: '🇰🇷 South Korea',
      careerGoals: 67, careerAssists: 28, careerMatches: 120,
      seasonGoals: 12, seasonAssists: 5, seasonMatches: 18, rating: 8.7
    },
    { 
      id: 6, name: 'David Martinez', position: 'Midfielder', status: 'Active',
      photo: 'DM', age: 26, height: '5\'9"', weight: '160 lbs', nationality: '🇪🇸 Spain',
      careerGoals: 34, careerAssists: 56, careerMatches: 150,
      seasonGoals: 4, seasonAssists: 9, seasonMatches: 20, rating: 8.4
    },
  ];

  const performanceData = [
    { month: 'Jan', goals: 3, assists: 2, rating: 8.5 },
    { month: 'Feb', goals: 4, assists: 1, rating: 8.7 },
    { month: 'Mar', goals: 5, assists: 2, rating: 9.0 },
    { month: 'Apr', goals: 4, assists: 1, rating: 8.8 },
    { month: 'May', goals: 2, assists: 1, rating: 8.4 },
  ];

  const matchHistory = [
    { date: '2025-05-05', opponent: 'Blue Thunder FC', result: 'Win', score: '3-1', goals: 2, assists: 1, rating: 9.2 },
    { date: '2025-04-28', opponent: 'Red Dragons', result: 'Draw', score: '2-2', goals: 1, assists: 0, rating: 8.5 },
    { date: '2025-04-21', opponent: 'Silver Knights', result: 'Win', score: '4-0', goals: 1, assists: 2, rating: 9.0 },
    { date: '2025-04-14', opponent: 'Green Warriors', result: 'Win', score: '2-1', goals: 0, assists: 1, rating: 8.3 },
  ];

  const trainingAttendance = [
    { date: '2025-05-07', type: 'Team Training', attended: true, duration: '90 min', intensity: 'High' },
    { date: '2025-05-06', type: 'Tactical Session', attended: true, duration: '60 min', intensity: 'Medium' },
    { date: '2025-05-04', type: 'Recovery Session', attended: true, duration: '45 min', intensity: 'Low' },
    { date: '2025-05-03', type: 'Team Training', attended: false, duration: '-', intensity: '-' },
    { date: '2025-05-02', type: 'Gym Session', attended: true, duration: '75 min', intensity: 'High' },
  ];

  const trainingCycle = [
    { day: 'J-7', date: '2025-05-01', type: 'Recovery', status: 'rest', color: 'bg-slate-400' },
    { day: 'J-6', date: '2025-05-02', type: 'Gym Training', status: 'training', color: 'bg-blue-500' },
    { day: 'J-5', date: '2025-05-03', type: 'Team Training', status: 'training', color: 'bg-blue-500' },
    { day: 'J-4', date: '2025-05-04', type: 'Recovery', status: 'rest', color: 'bg-slate-400' },
    { day: 'J-3', date: '2025-05-05', type: 'Tactical Session', status: 'training', color: 'bg-blue-500' },
    { day: 'J-2', date: '2025-05-06', type: 'Light Training', status: 'training', color: 'bg-blue-400' },
    { day: 'J-1', date: '2025-05-07', type: 'Rest Day', status: 'rest', color: 'bg-slate-400' },
    { day: 'J-Day', date: '2025-05-08', type: 'Match Day', status: 'match', color: 'bg-blue-900' },
  ];

  const handleLogout = () => {
    localStorage.removeItem('keycloak_token');
    localStorage.removeItem('user_name');
    window.location.href = '/';
  };

  const handlePlayerClick = (player) => {
    setSelectedPlayer(player);
  };

  const handleBackToRoster = () => {
    setSelectedPlayer(null);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Active': return 'text-green-400 bg-green-600/20';
      case 'Injured': return 'text-red-400 bg-red-600/20';
      case 'Suspended': return 'text-yellow-400 bg-yellow-600/20';
      default: return 'text-slate-400 bg-slate-600/20';
    }
  };

  const filteredPlayers = players.filter(player => {
    const matchesSearch = player.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          player.position.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesPosition = filters.position === 'all' || player.position === filters.position;
    const matchesStatus = filters.status === 'all' || player.status === filters.status;

    return matchesSearch && matchesPosition && matchesStatus;
  });

  // Player Roster View
  if (!selectedPlayer) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        {/* Top Navigation Bar */}
        

        {/* Main Content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-white mb-2">Team Roster</h2>
            <p className="text-slate-400">View player profiles and performance data</p>
          </div>

          {/* Search and Filter Bar */}
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl mb-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Search */}
              <div className="md:col-span-1">
                <label className="block text-slate-400 text-sm mb-2">Search Players</label>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <input
                    type="text"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder="Search by name or position..."
                    className="w-full bg-slate-700/50 border border-slate-600 rounded-lg pl-10 pr-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
                  />
                </div>
              </div>

              {/* Position Filter */}
              <div>
                <label className="block text-slate-400 text-sm mb-2">Position</label>
                <select
                  value={filters.position}
                  onChange={(e) => setFilters({ ...filters, position: e.target.value })}
                  className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
                >
                  <option value="all">All Positions</option>
                  <option value="Forward">Forward</option>
                  <option value="Midfielder">Midfielder</option>
                  <option value="Defender">Defender</option>
                  <option value="Goalkeeper">Goalkeeper</option>
                </select>
              </div>

              {/* Status Filter */}
              <div>
                <label className="block text-slate-400 text-sm mb-2">Status</label>
                <select
                  value={filters.status}
                  onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                  className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
                >
                  <option value="all">All Status</option>
                  <option value="Active">Active</option>
                  <option value="Injured">Injured</option>
                  <option value="Suspended">Suspended</option>
                </select>
              </div>
            </div>
          </div>

          {/* Player Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredPlayers.map((player) => (
              <div
                key={player.id}
                onClick={() => handlePlayerClick(player)}
                className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl hover:shadow-2xl hover:border-blue-600/50 transition-all cursor-pointer group"
              >
                {/* Player Avatar */}
                <div className="flex items-center space-x-4 mb-4">
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-600 to-blue-800 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-lg group-hover:scale-110 transition-transform">
                    {player.photo}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-white mb-1">{player.name}</h3>
                    <p className="text-slate-400 text-sm">{player.position}</p>
                  </div>
                </div>

                {/* Status Badge */}
                <div className="mb-4">
                  <span className={`px-3 py-1 text-xs font-semibold rounded-full ${getStatusColor(player.status)}`}>
                    {player.status}
                  </span>
                </div>

                {/* Quick Stats */}
                <div className="grid grid-cols-3 gap-3 mb-4">
                  <div className="text-center">
                    <p className="text-2xl font-bold text-blue-400">{player.seasonGoals}</p>
                    <p className="text-xs text-slate-400">Goals</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-blue-400">{player.seasonAssists}</p>
                    <p className="text-xs text-slate-400">Assists</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-yellow-400">{player.rating}</p>
                    <p className="text-xs text-slate-400">Rating</p>
                  </div>
                </div>

                {/* View Profile Button */}
                <button className="w-full flex items-center justify-center space-x-2 py-2 bg-blue-600/20 text-blue-400 rounded-lg group-hover:bg-blue-600/30 transition-colors">
                  <span className="text-sm font-medium">View Profile</span>
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // Player Profile View
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Top Navigation Bar */}
      <nav className="bg-slate-800/80 backdrop-blur-lg border-b border-slate-700/50 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <button
                onClick={handleBackToRoster}
                className="p-2 hover:bg-slate-700/50 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-5 h-5 text-slate-400 hover:text-white" />
              </button>
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center shadow-lg">
                <TrendingUp className="w-6 h-6 text-white" strokeWidth={2.5} />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">Sports Analytics</h1>
                <p className="text-xs text-slate-400">Player Profile</p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <button className="relative p-2 text-slate-400 hover:text-white hover:bg-slate-700/50 rounded-lg transition-colors">
                <Bell className="w-5 h-5" />
              </button>

              <div className="flex items-center space-x-3 px-3 py-2 bg-slate-700/50 rounded-lg">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-700 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                  {user.name.charAt(0)}
                </div>
                <div className="hidden sm:block">
                  <p className="text-sm font-medium text-white">{user.name}</p>
                  <p className="text-xs text-slate-400">{user.email}</p>
                </div>
              </div>

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
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Player Header Card */}
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-8 border border-slate-700/50 shadow-xl mb-6">
          <div className="flex flex-col md:flex-row items-start md:items-center space-y-6 md:space-y-0 md:space-x-8">
            {/* Avatar */}
            <div className="w-32 h-32 bg-gradient-to-br from-blue-600 to-blue-800 rounded-full flex items-center justify-center text-white text-5xl font-bold shadow-2xl">
              {selectedPlayer.photo}
            </div>

            {/* Player Info */}
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-3">
                <h2 className="text-4xl font-bold text-white">{selectedPlayer.name}</h2>
                <span className={`px-3 py-1 text-sm font-semibold rounded-full ${getStatusColor(selectedPlayer.status)}`}>
                  {selectedPlayer.status}
                </span>
              </div>
              <p className="text-blue-400 text-xl font-semibold mb-4">{selectedPlayer.position}</p>

              {/* Personal Details */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="flex items-center space-x-2">
                  <Calendar className="w-5 h-5 text-slate-400" />
                  <div>
                    <p className="text-xs text-slate-400">Age</p>
                    <p className="text-white font-semibold">{selectedPlayer.age} years</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Ruler className="w-5 h-5 text-slate-400" />
                  <div>
                    <p className="text-xs text-slate-400">Height</p>
                    <p className="text-white font-semibold">{selectedPlayer.height}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Weight className="w-5 h-5 text-slate-400" />
                  <div>
                    <p className="text-xs text-slate-400">Weight</p>
                    <p className="text-white font-semibold">{selectedPlayer.weight}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Flag className="w-5 h-5 text-slate-400" />
                  <div>
                    <p className="text-xs text-slate-400">Nationality</p>
                    <p className="text-white font-semibold">{selectedPlayer.nationality}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Career & Season Stats */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Career Stats */}
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
            <h3 className="text-xl font-bold text-blue-400 mb-6 flex items-center space-x-2">
              <Trophy className="w-6 h-6" />
              <span>Career Statistics</span>
            </h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg">
                <span className="text-slate-400">Total Matches</span>
                <span className="text-2xl font-bold text-white">{selectedPlayer.careerMatches}</span>
              </div>
              <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg">
                <span className="text-slate-400">Goals</span>
                <span className="text-2xl font-bold text-green-400">{selectedPlayer.careerGoals}</span>
              </div>
              <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg">
                <span className="text-slate-400">Assists</span>
                <span className="text-2xl font-bold text-blue-400">{selectedPlayer.careerAssists}</span>
              </div>
            </div>
          </div>

          {/* Season Stats */}
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
            <h3 className="text-xl font-bold text-blue-400 mb-6 flex items-center space-x-2">
              <Award className="w-6 h-6" />
              <span>2024/25 Season</span>
            </h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg">
                <span className="text-slate-400">Matches Played</span>
                <span className="text-2xl font-bold text-white">{selectedPlayer.seasonMatches}</span>
              </div>
              <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg">
                <span className="text-slate-400">Goals</span>
                <span className="text-2xl font-bold text-green-400">{selectedPlayer.seasonGoals}</span>
              </div>
              <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg">
                <span className="text-slate-400">Assists</span>
                <span className="text-2xl font-bold text-blue-400">{selectedPlayer.seasonAssists}</span>
              </div>
              <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg">
                <span className="text-slate-400">Average Rating</span>
                <span className="text-2xl font-bold text-yellow-400">{selectedPlayer.rating}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Performance Chart */}
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl mb-6">
          <h3 className="text-xl font-bold text-blue-400 mb-6">Performance Trend</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="month" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '8px' }}
                labelStyle={{ color: '#e2e8f0' }}
              />
              <Line type="monotone" dataKey="goals" stroke="#22c55e" strokeWidth={3} dot={{ fill: '#22c55e', r: 5 }} name="Goals" />
              <Line type="monotone" dataKey="assists" stroke="#3b82f6" strokeWidth={3} dot={{ fill: '#3b82f6', r: 5 }} name="Assists" />
              <Line type="monotone" dataKey="rating" stroke="#eab308" strokeWidth={3} dot={{ fill: '#eab308', r: 5 }} name="Rating" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Training Cycle Visualization */}
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl mb-6">
          <h3 className="text-xl font-bold text-blue-400 mb-6 flex items-center space-x-2">
            <Activity className="w-6 h-6" />
            <span>Training Cycle - Match Week</span>
          </h3>
          
          {/* Timeline */}
          <div className="relative">
            {/* Timeline Line */}
            <div className="absolute top-8 left-0 right-0 h-1 bg-slate-700"></div>
            
            {/* Timeline Items */}
            <div className="grid grid-cols-4 lg:grid-cols-8 gap-2">
              {trainingCycle.map((day, index) => (
                <div key={index} className="relative">
                  {/* Day Marker */}
                  <div className="flex flex-col items-center">
                    <div className={`w-16 h-16 ${day.color} rounded-full flex items-center justify-center shadow-lg z-10 border-4 border-slate-900 mb-3`}>
                      <span className="text-white font-bold text-sm">{day.day}</span>
                    </div>
                    <div className="text-center">
                      <p className="text-xs text-slate-400 mb-1">
                        {new Date(day.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                      </p>
                      <p className="text-xs text-white font-medium">{day.type}</p>
                      {day.status === 'training' && (
                        <Activity className="w-4 h-4 text-blue-400 mx-auto mt-1" />
                      )}
                      {day.status === 'rest' && (
                        <Heart className="w-4 h-4 text-slate-400 mx-auto mt-1" />
                      )}
                      {day.status === 'match' && (
                        <Trophy className="w-4 h-4 text-yellow-400 mx-auto mt-1" />
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Legend */}
          <div className="flex flex-wrap items-center justify-center gap-6 mt-8 pt-6 border-t border-slate-700/50">
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-blue-500 rounded-full"></div>
              <span className="text-sm text-slate-400">Training Session</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-slate-400 rounded-full"></div>
              <span className="text-sm text-slate-400">Rest/Recovery</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-blue-900 rounded-full"></div>
              <span className="text-sm text-slate-400">Match Day</span>
            </div>
          </div>
        </div>

        {/* Match History */}
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl mb-6">
          <h3 className="text-xl font-bold text-blue-400 mb-6 flex items-center space-x-2">
            <Trophy className="w-6 h-6" />
            <span>Recent Match History</span>
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-900/50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase">Date</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase">Opponent</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase">Result</th>
                  <th className="px-4 py-3 text-center text-xs font-semibold text-slate-400 uppercase">Score</th>
                  <th className="px-4 py-3 text-center text-xs font-semibold text-slate-400 uppercase">Goals</th>
                  <th className="px-4 py-3 text-center text-xs font-semibold text-slate-400 uppercase">Assists</th>
                  <th className="px-4 py-3 text-center text-xs font-semibold text-slate-400 uppercase">Rating</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/30">
                {matchHistory.map((match, index) => (
                  <tr key={index} className="hover:bg-slate-800/30">
                    <td className="px-4 py-3 whitespace-nowrap text-sm text-white">
                      {new Date(match.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm text-white font-medium">{match.opponent}</td>
                    <td className="px-4 py-3 whitespace-nowrap">
                      <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                        match.result === 'Win' ? 'text-green-400 bg-green-600/20' :
                        match.result === 'Draw' ? 'text-yellow-400 bg-yellow-600/20' :
                        'text-red-400 bg-red-600/20'
                      }`}>
                        {match.result}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center text-white font-semibold">{match.score}</td>
                    <td className="px-4 py-3 text-center text-green-400 font-bold">{match.goals}</td>
                    <td className="px-4 py-3 text-center text-blue-400 font-bold">{match.assists}</td>
                    <td className="px-4 py-3 text-center">
                      <span className="px-3 py-1 bg-yellow-600/20 text-yellow-400 text-sm font-bold rounded-full">
                        {match.rating}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Training Attendance */}
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
          <h3 className="text-xl font-bold text-blue-400 mb-6 flex items-center space-x-2">
            <Users className="w-6 h-6" />
            <span>Training Attendance Log</span>
          </h3>
          <div className="space-y-3">
            {trainingAttendance.map((session, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg hover:bg-slate-700/50 transition-colors">
                <div className="flex items-center space-x-4">
                  {session.attended ? (
                    <CheckCircle className="w-6 h-6 text-green-400 flex-shrink-0" />
                  ) : (
                    <XCircle className="w-6 h-6 text-red-400 flex-shrink-0" />
                  )}
                  <div>
                    <p className="text-white font-medium">{session.type}</p>
                    <p className="text-slate-400 text-sm">
                      {new Date(session.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-6">
                  <div className="text-right">
                    <p className="text-slate-400 text-xs">Duration</p>
                    <p className="text-white font-semibold">{session.duration}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-slate-400 text-xs">Intensity</p>
                    <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                      session.intensity === 'High' ? 'text-red-400 bg-red-600/20' :
                      session.intensity === 'Medium' ? 'text-yellow-400 bg-yellow-600/20' :
                      session.intensity === 'Low' ? 'text-green-400 bg-green-600/20' :
                      'text-slate-400 bg-slate-600/20'
                    }`}>
                      {session.intensity}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlayersPage;