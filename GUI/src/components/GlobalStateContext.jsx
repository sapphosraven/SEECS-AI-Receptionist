import React, { createContext, useContext, useState } from "react";

const GlobalStateContext = createContext();

export const GlobalStateProvider = ({ children }) => {
    const [isThinking, setIsThinking] = useState(false);

    return (
        <GlobalStateContext.Provider value={{ isThinking, setIsThinking }}>
            {children}
        </GlobalStateContext.Provider>
    );
};

export const useGlobalState = () => useContext(GlobalStateContext);
