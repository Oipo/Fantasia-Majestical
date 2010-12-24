if __name__ == '__main__':
    from rggSystem import injectMain
    main = injectMain()
    
    import rggSystem, rggRPC, rggChat, rggViews, rggRemote, rggEvent
    
    # Initialize view state.
    s = rggViews._state
    s.initialize()
    
    # EVENT WIRING
    # amounts to configuration
    
    # mouse events
    main.mouseMoveSignal.connect(rggEvent.mouseMoveEvent)
    main.mousePressSignal.connect(rggEvent.mousePressEvent)
    main.mouseReleaseSignal.connect(rggEvent.mouseReleaseEvent)
    
    # chat widget
    s.cwidget.chatInput.connect(rggEvent.chatInputEvent)
    
    # menu items
    s.menu.newMapAct.triggered.connect(rggViews.newMap)
    s.menu.loadMapAct.triggered.connect(rggViews.loadMap)
    s.menu.saveMapAct.triggered.connect(rggViews.saveMap)
    #s.menu.closeMapAct.triggered.connect(rggViews.closeAllMaps)
    #s.menu.saveCharsAct.triggered.connect(rggViews.saveChars)
    #s.menu.loadCharsAct.triggered.connect(rggViews.loadChars)
    s.menu.hostGameAct.triggered.connect(rggViews.hostGame)
    s.menu.joinGameAct.triggered.connect(rggViews.joinGame)
    s.menu.disconnectAct.triggered.connect(rggViews.disconnectGame)
    s.menu.thicknessOneAct.triggered.connect(rggViews.setThicknessToOne)
    s.menu.thicknessTwoAct.triggered.connect(rggViews.setThicknessToTwo)
    s.menu.thicknessThreeAct.triggered.connect(rggViews.setThicknessToThree)
    
    server = rggRPC.server
    client = rggRPC.client
    
    client.connected.connect(rggRemote.clientConnect)
    client.disconnected.connect(rggRemote.clientDisconnect)
    client.objectReceived.connect(rggRemote.clientReceive)
    client.fileReceived.connect(rggRemote.clientFileReceive)
    server.connected.connect(rggRemote.serverConnect)
    server.disconnected.connect(rggRemote.serverDisconnect)
    server.objectReceived.connect(rggRemote.serverReceive)
    server.fileReceived.connect(rggRemote.serverFileReceive)
    
    # Start execution
    try:
        main.start()
    finally:
        client.close()
