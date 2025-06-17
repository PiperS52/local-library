import {
  combineReducers,
  configureStore,
  PreloadedStateShapeFromReducersMapObject,
} from '@reduxjs/toolkit';

import { api } from './services/api';

const rootReducer = combineReducers({
  [api.reducerPath]: api.reducer,
});

export const setupStore = (
  preloadedState?: PreloadedStateShapeFromReducersMapObject<typeof rootReducer>
) => {
  return configureStore({
    reducer: rootReducer,
    preloadedState,
    middleware: (getDefaultMiddleware) =>
      getDefaultMiddleware().concat(api.middleware),
  });
};

export type RootState = ReturnType<typeof rootReducer>;
export type AppStore = ReturnType<typeof setupStore>;
export type AppDispatch = AppStore['dispatch'];
