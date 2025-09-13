import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Brain, Lightbulb, TrendingUp, MessageCircle } from "lucide-react";

interface AIInsight {
  id: string;
  type: "motivation" | "improvement" | "trend" | "tip";
  title: string;
  message: string;
  confidence: number;
}

const mockInsights: AIInsight[] = [
  {
    id: "1",
    type: "motivation",
    title: "Great Morning Routine!",
    message: "You've completed your morning habits 6 days in a row. This consistency is building strong neural pathways. Keep it up!",
    confidence: 92,
  },
  {
    id: "2",
    type: "improvement",
    title: "Optimization Suggestion",
    message: "Your workout completion rate drops on Wednesdays. Consider scheduling lighter exercises on this day.",
    confidence: 87,
  },
  {
    id: "3",
    type: "trend",
    title: "Positive Trend Detected",
    message: "Your meditation habit shows 23% improvement over the last two weeks. Stress levels likely decreasing!",
    confidence: 89,
  },
  {
    id: "4",
    type: "tip",
    title: "Habit Stacking Opportunity",
    message: "Link your reading habit with your evening tea routine for better consistency. Try reading 10 pages while having tea.",
    confidence: 94,
  },
];

const insightIcons = {
  motivation: MessageCircle,
  improvement: Lightbulb,
  trend: TrendingUp,
  tip: Brain,
};

const insightColors = {
  motivation: "bg-motivation text-motivation-foreground",
  improvement: "bg-primary text-primary-foreground",
  trend: "bg-secondary text-secondary-foreground",
  tip: "bg-accent text-accent-foreground",
};

export function AIInsights() {
  return (
    <Card className="p-6 bg-gradient-card shadow-habit-card border-0">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-primary/10">
          <Brain className="h-6 w-6 text-primary animate-glow" />
        </div>
        <h2 className="text-xl font-semibold text-foreground">AI Insights</h2>
        <Badge variant="secondary" className="bg-primary/10 text-primary">
          Smart Analytics
        </Badge>
      </div>

      <div className="space-y-4">
        {mockInsights.map((insight) => {
          const Icon = insightIcons[insight.type];
          return (
            <Card
              key={insight.id}
              className="p-4 bg-background/50 shadow-sm border hover:shadow-habit-card transition-all duration-300 hover:scale-[1.02]"
            >
              <div className="flex items-start gap-3">
                <div className={`p-2 rounded-lg ${insightColors[insight.type]}`}>
                  <Icon className="h-4 w-4" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="font-medium text-foreground">{insight.title}</h3>
                    <Badge variant="outline" className="text-xs">
                      {insight.confidence}% confidence
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {insight.message}
                  </p>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      <div className="mt-6 p-4 bg-primary/5 rounded-lg">
        <p className="text-sm text-muted-foreground text-center">
          💡 AI insights update every 24 hours based on your habit patterns and behavioral data.
        </p>
      </div>
    </Card>
  );
}