import { create } from "zustand";
import type { RosProject } from "./types";

interface AppStore {
  project: RosProject | null;
  setProject: (project: RosProject | null) => void;
  activeProfileId: string;
  setActiveProfileId: (profileId: string) => void;
}

export const useAppStore = create<AppStore>((set) => ({
  project: null,
  setProject: (project) => set({ project }),
  activeProfileId: "openai-account",
  setActiveProfileId: (activeProfileId) => set({ activeProfileId })
}));
