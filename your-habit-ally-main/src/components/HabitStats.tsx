import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, Target, Zap, Award } from "lucide-react";

interface HabitStatsProps {
  totalHabits: number;
  completedToday: number;
  longestStreak: number;
  weeklyCompletion: number;
}

export function HabitStats({
  totalHabits,
  completedToday,
  longestStreak,
  weeklyCompletion,
}: HabitStatsProps) {
  const completionPercentage = totalHabits > 0 ? (completedToday / totalHabits) * 100 : 0;

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <Card className="p-4 bg-gradient-card shadow-habit-card border-0 hover:shadow-floating transition-shadow">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-primary/10">
            <Target className="h-5 w-5 text-primary" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Today</p>
            <p className="text-2xl font-bold text-foreground">
              {completedToday}/{totalHabits}
            </p>
          </div>
        </div>
        <div className="mt-3">
          <div className="w-full bg-muted rounded-full h-2">
            <div
              className="bg-gradient-primary h-2 rounded-full transition-all duration-500"
              style={{ width: `${completionPercentage}%` }}
            />
          </div>
        </div>
      </Card>

      <Card className="p-4 bg-gradient-card shadow-habit-card border-0 hover:shadow-floating transition-shadow">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-motivation/10">
            <Zap className="h-5 w-5 text-motivation" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Best Streak</p>
            <p className="text-2xl font-bold text-foreground">{longestStreak}</p>
          </div>
        </div>
      </Card>

      <Card className="p-4 bg-gradient-card shadow-habit-card border-0 hover:shadow-floating transition-shadow">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-secondary/10">
            <TrendingUp className="h-5 w-5 text-secondary" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">This Week</p>
            <p className="text-2xl font-bold text-foreground">{weeklyCompletion}%</p>
          </div>
        </div>
      </Card>

      <Card className="p-4 bg-gradient-card shadow-habit-card border-0 hover:shadow-floating transition-shadow">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-accent/10">
            <Award className="h-5 w-5 text-accent-foreground" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Performance</p>
            <Badge 
              variant="secondary" 
              className={
                completionPercentage >= 80 
                  ? "bg-secondary text-secondary-foreground" 
                  : completionPercentage >= 60 
                  ? "bg-motivation text-motivation-foreground"
                  : "bg-warning text-warning-foreground"
              }
            >
              {completionPercentage >= 80 ? "Excellent" : completionPercentage >= 60 ? "Good" : "Improving"}
            </Badge>
          </div>
        </div>
      </Card>
    </div>
  );
}