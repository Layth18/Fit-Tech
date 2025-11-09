import React, { useState } from 'react';
import { 
  TrendingUp, LogOut, Bell, Search, Filter, Calendar, 
  MapPin, Trophy, ChevronDown, X, Target, Activity,
  Users, Clock, Flag, ArrowRight, TrendingDown, Award
} from 'lucide-react';

// Define types for our data structures
interface User {
  name: string;
  email: string;
}

interface Filters {
  dateFrom: string;
  dateTo: string;
  competition: string;
  homeAway: string;
  result: string;
}

interface Match {
  id: number;
  date: string;
  competition: string;
  opponent: string;
  homeAway: 'Home' | 'Away';
  result: 'Win' | 'Loss' | 'Draw';
  score: string;
  possession: number;
  shots: number;
  passAccuracy: number;
  tackles: number;
}

interface PlayerPerformance {
  name: string;
  position: string;
  goals: number;
  assists: number;
  rating: number;
  passes: number;
  shots: number;
}

const MatchesPage = () => {
  const [user] = useState<User>({ name: 'Demo User', email: 'demo@sports.com' });
  const [selectedMatch, setSelectedMatch] = useState<Match | null>(null);
  const [filters, setFilters] = useState<Filters>({
    dateFrom: '',
    dateTo: '',
    competition: 'all',
    homeAway: 'all',
    result: 'all'
  });

  const matches: Match[] = [
    { id: 1, date: '2025-05-05', competition: 'Premier League', opponent: 'Blue Thunder FC', homeAway: 'Home', result: 'Win', score: '3-1', possession: 58, shots: 15, passAccuracy: 84, tackles: 18 },
    { id: 2, date: '2025-04-28', competition: 'Premier League', opponent: 'Red Dragons', homeAway: 'Away', result: 'Draw', score: '2-2', possession: 52, shots: 12, passAccuracy: 79, tackles: 22 },
    { id: 3, date: '2025-04-21', competition: 'Cup', opponent: 'Silver Knights', homeAway: 'Home', result: 'Win', score: '4-0', possession: 65, shots: 18, passAccuracy: 87, tackles: 15 },
    { id: 4, date: '2025-04-14', competition: 'Premier League', opponent: 'Green Warriors', homeAway: 'Away', result: 'Win', score: '2-1', possession: 48, shots: 10, passAccuracy: 75, tackles: 25 },
    { id: 5, date: '2025-04-07', competition: 'Premier League', opponent: 'Gold Stars', homeAway: 'Home', result: 'Loss', score: '1-3', possession: 45, shots: 8, passAccuracy: 71, tackles: 20 },
  ];

  const playerPerformance: PlayerPerformance[] = [
    { name: 'John Doe', position: 'Forward', goals: 2, assists: 1, rating: 9.2, passes: 45, shots: 6 },
    { name: 'Mike Smith', position: 'Midfielder', goals: 1, assists: 2, rating: 8.8, passes: 68, shots: 3 },
    { name: 'Tom Brown', position: 'Defender', goals: 0, assists: 0, rating: 8.5, passes: 52, shots: 1 },
    { name: 'Alex Johnson', position: 'Goalkeeper', goals: 0, assists: 0, rating: 8.0, passes: 28, shots: 0 },
  ];

  const handleLogout = () => {
    localStorage.removeItem('keycloak_token');
    localStorage.removeItem('user_name');
    window.location.href = '/';
  };

  const handleMatchClick = (match: Match): void => {
    setSelectedMatch(match);
  };

  const closeMatchDetails = () => {
    setSelectedMatch(null);
  };

  const getResultColor = (result: string) => {
    switch (result) {
      case 'Win': return 'text-green-400 bg-green-600/20';
      case 'Loss': return 'text-red-400 bg-red-600/20';
      case 'Draw': return 'text-yellow-400 bg-yellow-600/20';
      default: return 'text-slate-400 bg-slate-600/20';
    }
  };

  const filteredMatches = matches.filter(match => {
    const matchDate = new Date(match.date);
    const fromDate = filters.dateFrom ? new Date(filters.dateFrom) : null;
    const toDate = filters.dateTo ? new Date(filters.dateTo) : null;

    if (fromDate && matchDate < fromDate) return false;
    if (toDate && matchDate > toDate) return false;
    if (filters.competition !== 'all' && match.competition !== filters.competition) return false;
    if (filters.homeAway !== 'all' && match.homeAway !== filters.homeAway) return false;
    if (filters.result !== 'all' && match.result !== filters.result) return false;

    return true;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search and Filter Bar */}
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            {/* Date From */}
            <div>
              <label className="block text-slate-400 text-sm mb-2">Date From</label>
              <input
                type="date"
                value={filters.dateFrom}
                onChange={(e) => setFilters({ ...filters, dateFrom: e.target.value })}
                className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
              />
            </div>

            {/* Date To */}
            <div>
              <label className="block text-slate-400 text-sm mb-2">Date To</label>
              <input
                type="date"
                value={filters.dateTo}
                onChange={(e) => setFilters({ ...filters, dateTo: e.target.value })}
                className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
              />
            </div>

            {/* Competition */}
            <div>
              <label className="block text-slate-400 text-sm mb-2">Competition</label>
              <select
                value={filters.competition}
                onChange={(e) => setFilters({ ...filters, competition: e.target.value })}
                className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
              >
                <option value="all">All Competitions</option>
                <option value="Premier League">Premier League</option>
                <option value="Cup">Cup</option>
              </select>
            </div>

            {/* Home/Away */}
            <div>
              <label className="block text-slate-400 text-sm mb-2">Home/Away</label>
              <select
                value={filters.homeAway}
                onChange={(e) => setFilters({ ...filters, homeAway: e.target.value })}
                className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
              >
                <option value="all">All</option>
                <option value="Home">Home</option>
                <option value="Away">Away</option>
              </select>
            </div>

            {/* Result */}
            <div>
              <label className="block text-slate-400 text-sm mb-2">Result</label>
              <select
                value={filters.result}
                onChange={(e) => setFilters({ ...filters, result: e.target.value })}
                className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
              >
                <option value="all">All Results</option>
                <option value="Win">Win</option>
                <option value="Draw">Draw</option>
                <option value="Loss">Loss</option>
              </select>
            </div>
          </div>
        </div>

        {/* Matches Table */}
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700/50 shadow-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-900/50">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-blue-400 uppercase tracking-wider">Date</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-blue-400 uppercase tracking-wider">Competition</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-blue-400 uppercase tracking-wider">Opponent</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-blue-400 uppercase tracking-wider">Home/Away</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-blue-400 uppercase tracking-wider">Result</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-blue-400 uppercase tracking-wider">Score</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-blue-400 uppercase tracking-wider"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/50">
                {filteredMatches.map((match) => (
                  <tr
                    key={match.id}
                    onClick={() => handleMatchClick(match)}
                    className="hover:bg-slate-700/30 cursor-pointer transition-colors"
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-white">
                      {new Date(match.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-3 py-1 bg-blue-600/20 text-blue-400 text-xs font-semibold rounded-full">
                        {match.competition}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-white font-medium">{match.opponent}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`flex items-center space-x-1 text-sm ${match.homeAway === 'Home' ? 'text-green-400' : 'text-slate-400'}`}>
                        <MapPin className="w-4 h-4" />
                        <span>{match.homeAway}</span>
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-3 py-1 text-xs font-semibold rounded-full ${getResultColor(match.result)}`}>
                        {match.result}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-lg font-bold text-white">{match.score}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-right">
                      <ArrowRight className="w-5 h-5 text-blue-400" />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Match Details Modal - FIXED VERSION */}
      {selectedMatch && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 rounded-2xl max-w-6xl w-full max-h-[90vh] border border-slate-700/50 shadow-2xl flex flex-col">
            {/* Header - Fixed */}
            <div className="flex items-center justify-between p-4 border-b border-slate-700/50 flex-shrink-0">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center">
                  <Trophy className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white">Match Details</h3>
                  <p className="text-slate-400 text-sm">{selectedMatch.opponent}</p>
                </div>
              </div>
              <button
                onClick={closeMatchDetails}
                className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
              >
                <X className="w-5 h-5 text-slate-400 hover:text-white" />
              </button>
            </div>

            {/* Scrollable Content */}
            <div className="overflow-y-auto flex-1 p-4 space-y-4">
              {/* Match Summary */}
              <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border border-slate-700/50">
                <h4 className="text-base font-semibold text-blue-400 mb-3">Match Summary</h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <p className="text-slate-400 text-xs mb-1">Score</p>
                    <p className="text-3xl font-bold text-white">{selectedMatch.score}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-slate-400 text-xs mb-1">Date</p>
                    <p className="text-sm font-semibold text-white">
                      {new Date(selectedMatch.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-slate-400 text-xs mb-1">Competition</p>
                    <span className="inline-block px-3 py-1 bg-blue-600/20 text-blue-400 text-xs font-semibold rounded-full">
                      {selectedMatch.competition}
                    </span>
                  </div>
                  <div className="text-center">
                    <p className="text-slate-400 text-xs mb-1">Result</p>
                    <span className={`inline-block px-3 py-1 text-xs font-semibold rounded-full ${getResultColor(selectedMatch.result)}`}>
                      {selectedMatch.result}
                    </span>
                  </div>
                </div>
              </div>

              {/* Team Statistics */}
              <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border border-slate-700/50">
                <h4 className="text-base font-semibold text-blue-400 mb-4">Team Statistics</h4>
                <div className="space-y-4">
                  {/* Possession */}
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-white text-sm font-medium">Possession</span>
                      <span className="text-blue-400 font-bold text-sm">{selectedMatch.possession}%</span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-blue-600 to-blue-400 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${selectedMatch.possession}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Stats Grid */}
                  <div className="grid grid-cols-3 gap-3">
                    <div className="bg-slate-800/50 rounded-lg p-3 text-center">
                      <Target className="w-5 h-5 text-blue-400 mx-auto mb-1" />
                      <p className="text-xl font-bold text-white mb-0.5">{selectedMatch.shots}</p>
                      <p className="text-slate-400 text-xs">Shots</p>
                    </div>
                    <div className="bg-slate-800/50 rounded-lg p-3 text-center">
                      <Activity className="w-5 h-5 text-green-400 mx-auto mb-1" />
                      <p className="text-xl font-bold text-white mb-0.5">{selectedMatch.passAccuracy}%</p>
                      <p className="text-slate-400 text-xs">Pass Accuracy</p>
                    </div>
                    <div className="bg-slate-800/50 rounded-lg p-3 text-center">
                      <Flag className="w-5 h-5 text-yellow-400 mx-auto mb-1" />
                      <p className="text-xl font-bold text-white mb-0.5">{selectedMatch.tackles}</p>
                      <p className="text-slate-400 text-xs">Tackles</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Player Performance Table */}
              <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border border-slate-700/50">
                <h4 className="text-base font-semibold text-blue-400 mb-3">Player Performance</h4>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-slate-900/50">
                      <tr>
                        <th className="px-3 py-2 text-left text-xs font-semibold text-slate-400 uppercase">Player</th>
                        <th className="px-3 py-2 text-left text-xs font-semibold text-slate-400 uppercase">Position</th>
                        <th className="px-3 py-2 text-center text-xs font-semibold text-slate-400 uppercase">Goals</th>
                        <th className="px-3 py-2 text-center text-xs font-semibold text-slate-400 uppercase">Assists</th>
                        <th className="px-3 py-2 text-center text-xs font-semibold text-slate-400 uppercase">Rating</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-700/30">
                      {playerPerformance.map((player, index) => (
                        <tr key={index} className="hover:bg-slate-800/30">
                          <td className="px-3 py-2 text-white font-medium">{player.name}</td>
                          <td className="px-3 py-2 text-slate-400 text-xs">{player.position}</td>
                          <td className="px-3 py-2 text-center text-white font-semibold">{player.goals}</td>
                          <td className="px-3 py-2 text-center text-white font-semibold">{player.assists}</td>
                          <td className="px-3 py-2 text-center">
                            <span className="px-2 py-1 bg-yellow-600/20 text-yellow-400 text-xs font-bold rounded-full">
                              {player.rating}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Visualizations Placeholder */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Heatmap Placeholder */}
                <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border border-slate-700/50">
                  <h4 className="text-base font-semibold text-blue-400 mb-3">Player Heatmap</h4>
                  <div className="aspect-video bg-slate-900/50 rounded-lg flex items-center justify-center border-2 border-dashed border-slate-700">
                    <div className="text-center">
                      <Activity className="w-10 h-10 text-slate-600 mx-auto mb-2" />
                      <p className="text-slate-500 text-xs">Heatmap Visualization</p>
                    </div>
                  </div>
                </div>

                {/* Shot Chart Placeholder */}
                <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border border-slate-700/50">
                  <h4 className="text-base font-semibold text-blue-400 mb-3">Shot Chart</h4>
                  <div className="aspect-video bg-slate-900/50 rounded-lg flex items-center justify-center border-2 border-dashed border-slate-700">
                    <div className="text-center">
                      <Target className="w-10 h-10 text-slate-600 mx-auto mb-2" />
                      <p className="text-slate-500 text-xs">Shot Chart Visualization</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MatchesPage;