--MM_TEST_IMPORT  ..\..\..\examples\ospray\ls1_co2_merker.lua
mmSetGUIVisible(false)
mmSetParamValue("::OSPRayRenderer_1::SamplesPerPixel",[=[20]=])
mmRenderNextFrame()
mmRenderNextFrame()
mmScreenshot("result.png")
mmQuit()
