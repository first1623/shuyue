import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import systemReducer from './slices/systemSlice';
import knowledgeTreeReducer from './slices/knowledgeTreeSlice';
import documentReducer from './slices/documentSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    system: systemReducer,
    knowledgeTree: knowledgeTreeReducer,
    document: documentReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
