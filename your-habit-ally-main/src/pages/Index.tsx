import { useState } from "react";
import { HabitCard } from "@/components/HabitCard";
import { HabitStats } from "@/components/HabitStats";
import { AIInsights } from "@/components/AIInsights";
import { AddHabitDialog } from "@/components/AddHabitDialog";
import { Brain, Calendar, Sparkles } from "lucide-react";
import { toast } from "@/hooks/use-toast";

interface Habit {
  id: string;
  name: string;
  description: string;
  streak: number;
  completed: boolean;
  category: "health" | "productivity" | "wellness" | "learning";
  completionRate: number;
}

const initialHabits: Habit[] = [
  {
    id: "1",
    name: "Morning Meditation",
    description: "10 minutes of mindfulness to start the day",
    streak: 7,
    completed: true,
    category: "wellness",
    completionRate: 86,
  },
  {
    id: "2",
    name: "Daily Exercise",
    description: "30 minutes of physical activity",
    streak: 4,
    completed: false,
    category: "health",
    completionRate: 71,
  },
  {
    id: "3",
    name: "Read 20 Pages",
    description: "Expand knowledge through daily reading",
    streak: 12,
    completed: true,
    category: "learning",
    completionRate: 92,
  },
  {
    id: "4",
    name: "Drink 8 Glasses Water",
    description: "Stay hydrated throughout the day",
    streak: 2,
    completed: false,
    category: "health",
    completionRate: 65,
  },
  {
    id: "5",
    name: "Deep Work Session",
    description: "2 hours of focused, uninterrupted work",
    streak: 3,
    completed: true,
    category: "productivity",
    completionRate: 78,
  },
];

const Index = () => {
  const [habits, setHabits] = useState<Habit[]>(initialHabits);

  const handleToggleHabit = (id: string) => {
    setHabits(habits.map(habit => 
      habit.id === id 
        ? { 
            ...habit, 
            completed: !habit.completed,
            streak: !habit.completed ? habit.streak + 1 : Math.max(0, habit.streak - 1)
          }
        : habit
    ));
    
    const habit = habits.find(h => h.id === id);
    if (habit && !habit.completed) {
      toast({
        title: "Great job! 🎉",
        description: `You completed "${habit.name}". Keep up the momentum!`,
      });
    }
  };

  const handleAddHabit = (newHabitData: { name: string; description: string; category: "health" | "productivity" | "wellness" | "learning" }) => {
    const newHabit: Habit = {
      id: Date.now().toString(),
      ...newHabitData,
      streak: 0,
      completed: false,
      completionRate: 0,
    };
    setHabits([...habits, newHabit]);
    toast({
      title: "New habit created! 🌟",
      description: `"${newHabit.name}" has been added to your routine.`,
    });
  };

  const completedToday = habits.filter(h => h.completed).length;
  const longestStreak = Math.max(...habits.map(h => h.streak));
  const weeklyCompletion = Math.round(habits.reduce((acc, h) => acc + h.completionRate, 0) / habits.length);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card/50 backdrop-blur supports-[backdrop-filter]:bg-card/50">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-gradient-primary">
                <Brain className="h-6 w-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">Smart Habit Tracker</h1>
                <p className="text-muted-foreground">Build better habits with AI-powered insights</p>
              </div>
            </div>
            <AddHabitDialog onAddHabit={handleAddHabit} />
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 space-y-8">
        {/* Stats Overview */}
        <section>
          <div className="flex items-center gap-2 mb-6">
            <Calendar className="h-5 w-5 text-primary" />
            <h2 className="text-xl font-semibold text-foreground">Today's Progress</h2>
          </div>
          <HabitStats
            totalHabits={habits.length}
            completedToday={completedToday}
            longestStreak={longestStreak}
            weeklyCompletion={weeklyCompletion}
          />
        </section>

        {/* Habits Grid */}
        <section>
          <div className="flex items-center gap-2 mb-6">
            <Sparkles className="h-5 w-5 text-primary" />
            <h2 className="text-xl font-semibold text-foreground">Your Habits</h2>
          </div>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {habits.map((habit) => (
              <HabitCard
                key={habit.id}
                {...habit}
                onToggle={handleToggleHabit}
              />
            ))}
          </div>
        </section>

        {/* AI Insights */}
        <section>
          <AIInsights />
        </section>
      </main>
    </div>
  );
};

export default Index;
