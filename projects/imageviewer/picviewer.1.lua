--MM_TEST_IMPORT  ..\..\..\examples\imageviewer\picviewer.lua
mmSetGUIVisible(false)
mmRenderNextFrame()
mmRenderNextFrame()
mmScreenshot("result.png")
mmQuit()
