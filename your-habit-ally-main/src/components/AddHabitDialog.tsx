import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Plus } from "lucide-react";

interface NewHabit {
  name: string;
  description: string;
  category: "health" | "productivity" | "wellness" | "learning";
}

interface AddHabitDialogProps {
  onAddHabit: (habit: NewHabit) => void;
}

export function AddHabitDialog({ onAddHabit }: AddHabitDialogProps) {
  const [open, setOpen] = useState(false);
  const [newHabit, setNewHabit] = useState<NewHabit>({
    name: "",
    description: "",
    category: "health",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (newHabit.name.trim()) {
      onAddHabit(newHabit);
      setNewHabit({ name: "", description: "", category: "health" });
      setOpen(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="bg-gradient-primary hover:opacity-90 shadow-floating">
          <Plus className="h-4 w-4 mr-2" />
          Add New Habit
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md bg-card border-0 shadow-floating">
        <DialogHeader>
          <DialogTitle className="text-xl font-semibold text-foreground">
            Create New Habit
          </DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="name" className="text-sm font-medium text-foreground">
              Habit Name
            </Label>
            <Input
              id="name"
              placeholder="e.g., Drink 8 glasses of water"
              value={newHabit.name}
              onChange={(e) => setNewHabit({ ...newHabit, name: e.target.value })}
              className="mt-1"
              required
            />
          </div>
          
          <div>
            <Label htmlFor="description" className="text-sm font-medium text-foreground">
              Description
            </Label>
            <Textarea
              id="description"
              placeholder="Why is this habit important to you?"
              value={newHabit.description}
              onChange={(e) => setNewHabit({ ...newHabit, description: e.target.value })}
              className="mt-1 resize-none"
              rows={3}
            />
          </div>
          
          <div>
            <Label htmlFor="category" className="text-sm font-medium text-foreground">
              Category
            </Label>
            <Select
              value={newHabit.category}
              onValueChange={(value: "health" | "productivity" | "wellness" | "learning") =>
                setNewHabit({ ...newHabit, category: value })
              }
            >
              <SelectTrigger className="mt-1">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="health">🏃‍♂️ Health</SelectItem>
                <SelectItem value="productivity">⚡ Productivity</SelectItem>
                <SelectItem value="wellness">🧘‍♀️ Wellness</SelectItem>
                <SelectItem value="learning">📚 Learning</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div className="flex gap-3 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => setOpen(false)}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              className="flex-1 bg-gradient-primary hover:opacity-90"
            >
              Create Habit
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}