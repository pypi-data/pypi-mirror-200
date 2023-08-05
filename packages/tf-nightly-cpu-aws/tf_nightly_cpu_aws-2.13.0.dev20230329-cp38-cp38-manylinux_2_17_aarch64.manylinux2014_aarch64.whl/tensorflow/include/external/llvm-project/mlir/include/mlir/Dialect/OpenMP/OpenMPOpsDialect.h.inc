/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Dialect Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace omp {

class OpenMPDialect : public ::mlir::Dialect {
  explicit OpenMPDialect(::mlir::MLIRContext *context);

  void initialize();
  friend class ::mlir::MLIRContext;
public:
  ~OpenMPDialect() override;
  static constexpr ::llvm::StringLiteral getDialectNamespace() {
    return ::llvm::StringLiteral("omp");
  }

  /// Parse an attribute registered to this dialect.
  ::mlir::Attribute parseAttribute(::mlir::DialectAsmParser &parser,
                                   ::mlir::Type type) const override;

  /// Print an attribute registered to this dialect.
  void printAttribute(::mlir::Attribute attr,
                      ::mlir::DialectAsmPrinter &os) const override;

    // Set the omp.is_device attribute on the module with the specified boolean
    static void setIsDevice(Operation* module, bool isDevice);

    // Return the value of the omp.is_device attribute stored in the module if it
    // exists, otherwise return false by default
    static bool getIsDevice(Operation* module);
  };
} // namespace omp
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::omp::OpenMPDialect)
