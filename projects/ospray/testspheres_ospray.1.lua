--MM_TEST_IMPORT  ..\..\..\examples\ospray\testspheres_ospray.lua
mmSetGUIVisible(false)
mmSetParamValue("::OSPRayRenderer_1::SamplesPerPixel",[=[20]=])
mmRenderNextFrame()
mmRenderNextFrame()
mmScreenshot("result.png")
mmQuit()
