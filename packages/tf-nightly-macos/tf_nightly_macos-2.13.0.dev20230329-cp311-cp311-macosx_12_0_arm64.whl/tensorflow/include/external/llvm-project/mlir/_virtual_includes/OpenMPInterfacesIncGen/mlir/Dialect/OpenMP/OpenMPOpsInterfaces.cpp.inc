/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Definitions                                                      *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

/// Set the attribute IsDeviceAttr on the current module with the 
/// specified boolean argument. 
void mlir::omp::OffloadModuleInterface::setIsDevice(bool isDevice) {
      return getImpl()->setIsDevice(getImpl(), getOperation(), isDevice);
  }
/// Get the IsDeviceAttr attribute on the current module if it exists and return
/// its value, if it doesn't exit it returns false by default.
bool mlir::omp::OffloadModuleInterface::getIsDevice() {
      return getImpl()->getIsDevice(getImpl(), getOperation());
  }
/// Get alloca block
::mlir::Block*mlir::omp::OutlineableOpenMPOpInterface::getAllocaBlock() {
      return getImpl()->getAllocaBlock(getImpl(), getOperation());
  }
/// Get reduction vars
::mlir::SmallVector<::mlir::Value> mlir::omp::ReductionClauseInterface::getAllReductionVars() {
      return getImpl()->getAllReductionVars(getImpl(), getOperation());
  }
