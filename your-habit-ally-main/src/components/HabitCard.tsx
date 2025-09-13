import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { CheckCircle, Circle, Flame, Target } from "lucide-react";
import { cn } from "@/lib/utils";

interface HabitCardProps {
  id: string;
  name: string;
  description: string;
  streak: number;
  completed: boolean;
  category: "health" | "productivity" | "wellness" | "learning";
  completionRate: number;
  onToggle: (id: string) => void;
}

const categoryColors = {
  health: "bg-secondary text-secondary-foreground",
  productivity: "bg-primary text-primary-foreground",
  wellness: "bg-accent text-accent-foreground",
  learning: "bg-motivation text-motivation-foreground",
};

export function HabitCard({
  id,
  name,
  description,
  streak,
  completed,
  category,
  completionRate,
  onToggle,
}: HabitCardProps) {
  const [isAnimating, setIsAnimating] = useState(false);

  const handleToggle = () => {
    if (!completed) {
      setIsAnimating(true);
      setTimeout(() => setIsAnimating(false), 600);
    }
    onToggle(id);
  };

  return (
    <Card
      className={cn(
        "p-6 transition-all duration-300 hover:shadow-floating bg-gradient-card border-0",
        completed ? "shadow-completed bg-gradient-success" : "shadow-habit-card"
      )}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h3 className={cn(
              "font-semibold text-lg transition-colors",
              completed ? "text-secondary-foreground" : "text-foreground"
            )}>
              {name}
            </h3>
            <Badge className={categoryColors[category]} variant="secondary">
              {category}
            </Badge>
          </div>
          <p className={cn(
            "text-sm transition-colors",
            completed ? "text-secondary-foreground/80" : "text-muted-foreground"
          )}>
            {description}
          </p>
        </div>
        
        <Button
          variant="ghost"
          size="sm"
          onClick={handleToggle}
          className={cn(
            "ml-4 p-2 rounded-full transition-all duration-300 hover:scale-110",
            completed 
              ? "text-secondary-foreground hover:bg-secondary-foreground/10" 
              : "text-primary hover:bg-primary/10",
            isAnimating && "animate-habit-complete"
          )}
        >
          {completed ? (
            <CheckCircle className="h-6 w-6" />
          ) : (
            <Circle className="h-6 w-6" />
          )}
        </Button>
      </div>

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1">
            <Flame className={cn(
              "h-4 w-4",
              streak > 0 ? "text-motivation" : "text-muted-foreground"
            )} />
            <span className={cn(
              "text-sm font-medium",
              streak > 0 ? "text-motivation" : "text-muted-foreground"
            )}>
              {streak} day streak
            </span>
          </div>
          
          <div className="flex items-center gap-1">
            <Target className="h-4 w-4 text-primary" />
            <span className="text-sm font-medium text-primary">
              {completionRate}% this week
            </span>
          </div>
        </div>
      </div>
    </Card>
  );
}