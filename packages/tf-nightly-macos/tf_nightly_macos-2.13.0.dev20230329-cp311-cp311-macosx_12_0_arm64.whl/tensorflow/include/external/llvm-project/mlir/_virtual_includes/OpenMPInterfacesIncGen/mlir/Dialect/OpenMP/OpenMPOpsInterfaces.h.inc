/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace omp {
class OffloadModuleInterface;
namespace detail {
struct OffloadModuleInterfaceInterfaceTraits {
  struct Concept {
    /// The methods defined by the interface.
    void (*setIsDevice)(const Concept *impl, ::mlir::Operation *, bool);
    bool (*getIsDevice)(const Concept *impl, ::mlir::Operation *);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = ::mlir::omp::OffloadModuleInterface;
    Model() : Concept{setIsDevice, getIsDevice} {}

    static inline void setIsDevice(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, bool isDevice);
    static inline bool getIsDevice(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::omp::OffloadModuleInterface;
    FallbackModel() : Concept{setIsDevice, getIsDevice} {}

    static inline void setIsDevice(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, bool isDevice);
    static inline bool getIsDevice(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteOp;
    void setIsDevice(::mlir::Operation *tablegen_opaque_val, bool isDevice) const;
    bool getIsDevice(::mlir::Operation *tablegen_opaque_val) const;
  };
};template <typename ConcreteOp>
struct OffloadModuleInterfaceTrait;

} // namespace detail
class OffloadModuleInterface : public ::mlir::OpInterface<OffloadModuleInterface, detail::OffloadModuleInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<OffloadModuleInterface, detail::OffloadModuleInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::OffloadModuleInterfaceTrait<ConcreteOp> {};
  /// Set the attribute IsDeviceAttr on the current module with the 
  /// specified boolean argument. 
  void setIsDevice(bool isDevice);
  /// Get the IsDeviceAttr attribute on the current module if it exists and return
  /// its value, if it doesn't exit it returns false by default.
  bool getIsDevice();
};
namespace detail {
  template <typename ConcreteOp>
  struct OffloadModuleInterfaceTrait : public ::mlir::OpInterface<OffloadModuleInterface, detail::OffloadModuleInterfaceInterfaceTraits>::Trait<ConcreteOp> {
    /// Set the attribute IsDeviceAttr on the current module with the 
    /// specified boolean argument. 
    void setIsDevice(bool isDevice) {
      (*static_cast<ConcreteOp *>(this))->setAttr(
          mlir::StringAttr::get((*static_cast<ConcreteOp *>(this))->getContext(), llvm::Twine{"omp.is_device"}),
            mlir::omp::IsDeviceAttr::get((*static_cast<ConcreteOp *>(this))->getContext(), isDevice));
    }
    /// Get the IsDeviceAttr attribute on the current module if it exists and return
    /// its value, if it doesn't exit it returns false by default.
    bool getIsDevice() {
      if (Attribute isDevice = (*static_cast<ConcreteOp *>(this))->getAttr("omp.is_device"))
          if (isDevice.isa<mlir::omp::IsDeviceAttr>())
            return isDevice.dyn_cast<IsDeviceAttr>().getIsDevice();
        return false;
    }
  };
}// namespace detail
} // namespace omp
} // namespace mlir
namespace mlir {
namespace omp {
class OutlineableOpenMPOpInterface;
namespace detail {
struct OutlineableOpenMPOpInterfaceInterfaceTraits {
  struct Concept {
    /// The methods defined by the interface.
    ::mlir::Block*(*getAllocaBlock)(const Concept *impl, ::mlir::Operation *);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = ::mlir::omp::OutlineableOpenMPOpInterface;
    Model() : Concept{getAllocaBlock} {}

    static inline ::mlir::Block*getAllocaBlock(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::omp::OutlineableOpenMPOpInterface;
    FallbackModel() : Concept{getAllocaBlock} {}

    static inline ::mlir::Block*getAllocaBlock(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteOp;
  };
};template <typename ConcreteOp>
struct OutlineableOpenMPOpInterfaceTrait;

} // namespace detail
class OutlineableOpenMPOpInterface : public ::mlir::OpInterface<OutlineableOpenMPOpInterface, detail::OutlineableOpenMPOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<OutlineableOpenMPOpInterface, detail::OutlineableOpenMPOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::OutlineableOpenMPOpInterfaceTrait<ConcreteOp> {};
  /// Get alloca block
  ::mlir::Block*getAllocaBlock();
};
namespace detail {
  template <typename ConcreteOp>
  struct OutlineableOpenMPOpInterfaceTrait : public ::mlir::OpInterface<OutlineableOpenMPOpInterface, detail::OutlineableOpenMPOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
} // namespace omp
} // namespace mlir
namespace mlir {
namespace omp {
class ReductionClauseInterface;
namespace detail {
struct ReductionClauseInterfaceInterfaceTraits {
  struct Concept {
    /// The methods defined by the interface.
    ::mlir::SmallVector<::mlir::Value> (*getAllReductionVars)(const Concept *impl, ::mlir::Operation *);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = ::mlir::omp::ReductionClauseInterface;
    Model() : Concept{getAllReductionVars} {}

    static inline ::mlir::SmallVector<::mlir::Value> getAllReductionVars(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::omp::ReductionClauseInterface;
    FallbackModel() : Concept{getAllReductionVars} {}

    static inline ::mlir::SmallVector<::mlir::Value> getAllReductionVars(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteOp;
    ::mlir::SmallVector<::mlir::Value> getAllReductionVars(::mlir::Operation *tablegen_opaque_val) const;
  };
};template <typename ConcreteOp>
struct ReductionClauseInterfaceTrait;

} // namespace detail
class ReductionClauseInterface : public ::mlir::OpInterface<ReductionClauseInterface, detail::ReductionClauseInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<ReductionClauseInterface, detail::ReductionClauseInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::ReductionClauseInterfaceTrait<ConcreteOp> {};
  /// Get reduction vars
  ::mlir::SmallVector<::mlir::Value> getAllReductionVars();
};
namespace detail {
  template <typename ConcreteOp>
  struct ReductionClauseInterfaceTrait : public ::mlir::OpInterface<ReductionClauseInterface, detail::ReductionClauseInterfaceInterfaceTraits>::Trait<ConcreteOp> {
    /// Get reduction vars
    ::mlir::SmallVector<::mlir::Value> getAllReductionVars() {
      return (*static_cast<ConcreteOp *>(this)).getReductionVars();
    }
  };
}// namespace detail
} // namespace omp
} // namespace mlir
namespace mlir {
namespace omp {
template<typename ConcreteOp>
void detail::OffloadModuleInterfaceInterfaceTraits::Model<ConcreteOp>::setIsDevice(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, bool isDevice) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).setIsDevice(isDevice);
}
template<typename ConcreteOp>
bool detail::OffloadModuleInterfaceInterfaceTraits::Model<ConcreteOp>::getIsDevice(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getIsDevice();
}
template<typename ConcreteOp>
void detail::OffloadModuleInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::setIsDevice(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, bool isDevice) {
  return static_cast<const ConcreteOp *>(impl)->setIsDevice(tablegen_opaque_val, isDevice);
}
template<typename ConcreteOp>
bool detail::OffloadModuleInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getIsDevice(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getIsDevice(tablegen_opaque_val);
}
template<typename ConcreteModel, typename ConcreteOp>
void detail::OffloadModuleInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::setIsDevice(::mlir::Operation *tablegen_opaque_val, bool isDevice) const {
(llvm::cast<ConcreteOp>(tablegen_opaque_val))->setAttr(
          mlir::StringAttr::get((llvm::cast<ConcreteOp>(tablegen_opaque_val))->getContext(), llvm::Twine{"omp.is_device"}),
            mlir::omp::IsDeviceAttr::get((llvm::cast<ConcreteOp>(tablegen_opaque_val))->getContext(), isDevice));
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::OffloadModuleInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::getIsDevice(::mlir::Operation *tablegen_opaque_val) const {
if (Attribute isDevice = (llvm::cast<ConcreteOp>(tablegen_opaque_val))->getAttr("omp.is_device"))
          if (isDevice.isa<mlir::omp::IsDeviceAttr>())
            return isDevice.dyn_cast<IsDeviceAttr>().getIsDevice();
        return false;
}
} // namespace omp
} // namespace mlir
namespace mlir {
namespace omp {
template<typename ConcreteOp>
::mlir::Block*detail::OutlineableOpenMPOpInterfaceInterfaceTraits::Model<ConcreteOp>::getAllocaBlock(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return &(llvm::cast<ConcreteOp>(tablegen_opaque_val)).getRegion().front();
}
template<typename ConcreteOp>
::mlir::Block*detail::OutlineableOpenMPOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getAllocaBlock(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getAllocaBlock(tablegen_opaque_val);
}
} // namespace omp
} // namespace mlir
namespace mlir {
namespace omp {
template<typename ConcreteOp>
::mlir::SmallVector<::mlir::Value> detail::ReductionClauseInterfaceInterfaceTraits::Model<ConcreteOp>::getAllReductionVars(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getAllReductionVars();
}
template<typename ConcreteOp>
::mlir::SmallVector<::mlir::Value> detail::ReductionClauseInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getAllReductionVars(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getAllReductionVars(tablegen_opaque_val);
}
template<typename ConcreteModel, typename ConcreteOp>
::mlir::SmallVector<::mlir::Value> detail::ReductionClauseInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::getAllReductionVars(::mlir::Operation *tablegen_opaque_val) const {
return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getReductionVars();
}
} // namespace omp
} // namespace mlir
